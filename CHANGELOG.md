# Changelog

## Unreleased

- Preserve partial SSE lines and UTF-8 characters across OpenRouter response
  chunks. Stop at `[DONE]`, release the reader on completion or failure, and
  propagate callback errors instead of treating them as malformed JSON.
