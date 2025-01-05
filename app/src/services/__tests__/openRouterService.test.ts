import { testPrompt } from '../settingsService';

// Mock fetch
global.fetch = jest.fn();

describe('OpenRouter API Integration', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('testPrompt', () => {
    it('should handle streaming responses correctly', async () => {
      // Mock ReadableStream
      const mockStream = new ReadableStream({
        start(controller) {
          const responses = [
            'data: {"choices":[{"delta":{"content":"Hello"}}]}',
            'data: {"choices":[{"delta":{"content":" World"}}]}',
            'data: [DONE]'
          ];
          
          responses.forEach(response => controller.enqueue(new TextEncoder().encode(response + '\n')));
          controller.close();
        }
      });

      // Mock fetch response
      (global.fetch as jest.Mock).mockResolvedValue({
        ok: true,
        body: mockStream,
        status: 200
      });

      const chunks: string[] = [];
      const onChunk = (chunk: string) => chunks.push(chunk);

      await testPrompt('test-key', 'test-model', 'Hello', onChunk);

      expect(chunks).toEqual(['Hello', ' World']);
      expect(global.fetch).toHaveBeenCalledWith(
        'https://openrouter.ai/api/v1/chat/completions',
        expect.objectContaining({
          method: 'POST',
          headers: expect.objectContaining({
            'Authorization': 'Bearer test-key',
            'HTTP-Referer': expect.any(String),
            'X-Title': 'Symbolic Scribe'
          })
        })
      );
    });

    it('should handle API errors correctly', async () => {
      (global.fetch as jest.Mock).mockResolvedValue({
        ok: false,
        status: 401,
        json: () => Promise.resolve({ error: { message: 'Invalid API key' } })
      });

      await expect(testPrompt('invalid-key', 'test-model', 'test', jest.fn()))
        .rejects
        .toThrow('Invalid API key');
    });

    it('should handle network errors', async () => {
      (global.fetch as jest.Mock).mockRejectedValue(new Error('Network error'));

      await expect(testPrompt('test-key', 'test-model', 'test', jest.fn()))
        .rejects
        .toThrow('Network error');
    });

    it('should handle malformed stream data', async () => {
      const mockStream = new ReadableStream({
        start(controller) {
          controller.enqueue(new TextEncoder().encode('data: {malformed json}\n'));
          controller.close();
        }
      });

      (global.fetch as jest.Mock).mockResolvedValue({
        ok: true,
        body: mockStream,
        status: 200
      });

      const onChunk = jest.fn();
      await testPrompt('test-key', 'test-model', 'test', onChunk);
      
      expect(onChunk).not.toHaveBeenCalled();
    });
  });
});
