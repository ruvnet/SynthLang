import { openRouterService } from '../openRouterService';

const event = (content: string) => `data: ${JSON.stringify({ choices: [{ delta: { content } }] })}\n\n`;
const options = { model: 'test-model', messages: [], stream: true };

describe('OpenRouter response streaming', () => {
  const originalFetch = global.fetch;
  let parseError: jest.SpyInstance;

  beforeEach(() => {
    global.fetch = jest.fn();
    parseError = jest.spyOn(console, 'error').mockImplementation(() => {});
  });

  afterEach(() => {
    global.fetch = originalFetch;
    parseError.mockRestore();
  });

  function respond(chunks: Uint8Array[]) {
    let index = 0;
    const reader = {
      read: jest.fn(async () => index < chunks.length
        ? { done: false, value: chunks[index++] }
        : { done: true, value: undefined }),
      cancel: jest.fn(async () => {}),
      releaseLock: jest.fn(),
    };
    (global.fetch as jest.Mock).mockResolvedValue({ ok: true, body: { getReader: () => reader } });
    return reader;
  }

  it('preserves the response at every byte boundary, including UTF-8 characters', async () => {
    const bytes = new TextEncoder().encode(event('Hello café 世界 🚀'));
    for (let split = 1; split < bytes.length; split++) {
      respond([bytes.slice(0, split), bytes.slice(split)]);
      const onChunk = jest.fn();
      await openRouterService.streamCompletion({ ...options, onChunk }, 'test-key');
      expect({ split, chunks: onChunk.mock.calls }).toEqual({ split, chunks: [['Hello café 世界 🚀']] });
    }
    expect(parseError).not.toHaveBeenCalled();
  });

  it('handles one-byte chunks, CRLF, comments, and multiple events', async () => {
    const bytes = new TextEncoder().encode(`: keep-alive\n\n${event('one')}${event('two')}`.replace(/\n/g, '\r\n'));
    const reader = respond(Array.from(bytes, byte => new Uint8Array([byte])));
    const onChunk = jest.fn();
    await openRouterService.streamCompletion({ ...options, onChunk }, 'test-key');
    expect(onChunk.mock.calls).toEqual([['one'], ['two']]);
    expect(reader.releaseLock).toHaveBeenCalledTimes(1);
  });

  it('stops at DONE and releases the reader', async () => {
    const reader = respond([new TextEncoder().encode(`${event('one')}data: [DONE]\r\n\r\n${event('ignored')}`)]);
    const onChunk = jest.fn();
    await openRouterService.streamCompletion({ ...options, onChunk }, 'test-key');
    expect(onChunk.mock.calls).toEqual([['one']]);
    expect(reader.cancel).toHaveBeenCalledTimes(1);
    expect(reader.releaseLock).toHaveBeenCalledTimes(1);
  });

  it('processes the last line when EOF arrives without a newline', async () => {
    const reader = respond([new TextEncoder().encode(event('last').trimEnd())]);
    const onChunk = jest.fn();
    await openRouterService.streamCompletion({ ...options, onChunk }, 'test-key');
    expect(onChunk).toHaveBeenCalledWith('last');
    expect(reader.releaseLock).toHaveBeenCalledTimes(1);
  });

  it('skips malformed JSON and continues with subsequent events', async () => {
    respond([new TextEncoder().encode(`data: {invalid}\n\n${event('valid')}`)]);
    const onChunk = jest.fn();
    await openRouterService.streamCompletion({ ...options, onChunk }, 'test-key');
    expect(onChunk.mock.calls).toEqual([['valid']]);
    expect(parseError).toHaveBeenCalledTimes(1);
  });

  it('ignores null payloads and usage events without choices', async () => {
    respond([new TextEncoder().encode(`data: null\n\ndata: {"usage":{"total_tokens":1}}\n\n${event('valid')}`)]);
    const onChunk = jest.fn();
    await openRouterService.streamCompletion({ ...options, onChunk }, 'test-key');
    expect(onChunk.mock.calls).toEqual([['valid']]);
    expect(parseError).not.toHaveBeenCalled();
  });

  it('propagates read failures and releases the reader', async () => {
    const reader = respond([]);
    reader.read.mockRejectedValueOnce(new Error('connection lost'));
    await expect(openRouterService.streamCompletion(options, 'test-key')).rejects.toThrow('connection lost');
    expect(reader.releaseLock).toHaveBeenCalledTimes(1);
  });

  it('propagates callback failures and releases the reader', async () => {
    const reader = respond([new TextEncoder().encode(event('one'))]);
    const onChunk = () => { throw new Error('callback failed'); };
    await expect(openRouterService.streamCompletion({ ...options, onChunk }, 'test-key')).rejects.toThrow('callback failed');
    expect(reader.releaseLock).toHaveBeenCalledTimes(1);
    expect(parseError).not.toHaveBeenCalled();
  });

  it('returns JSON responses when streaming is disabled', async () => {
    const data = { choices: [{ message: { content: 'complete' } }] };
    const json = jest.fn().mockResolvedValue(data);
    (global.fetch as jest.Mock).mockResolvedValue({ ok: true, json });
    await expect(openRouterService.streamCompletion({ ...options, stream: false }, 'test-key')).resolves.toEqual(data);
    expect(json).toHaveBeenCalledTimes(1);
  });
});
