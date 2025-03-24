# Quick Start Guide

This guide will help you quickly set up and run SynthLang Proxy.

## Prerequisites

- Python 3.8+
- pip
- OpenAI API Key

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/synthlang-proxy.git
    cd synthlang-proxy/proxy
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure environment variables:**

    - Copy `.env.sample` to `.env`:
      ```bash
      cp .env.sample .env
      ```
    - Edit `.env` and set your `OPENAI_API_KEY` and other configurations as needed.

4.  **Run the proxy server:**

    ```bash
    cd src
    python -m app.main
    ```

    The proxy server will start at `http://localhost:8000`.

## Testing the Proxy

Send a test request to the proxy using `curl`:

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'
```

Replace `your_api_key` with your actual API key. You should receive a response from the LLM through the proxy.

## Next Steps

- Explore the [User Guide](user_guide.md) for detailed information on using SynthLang Proxy.
- Check out the [CLI Documentation](cli.md) for command-line tools.
- Learn about [Prompt Compression](synthlang_integration.md) and [Semantic Caching](README.md#semantic-caching) to optimize performance and costs.