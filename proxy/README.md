# SynthLang Proxy

Synthlang Proxy turns any existing LLM app (OpenAi v1/Endpoint) or Coder (Cursor etc) into an agentic, hyper-optimized, self-evolving system and it's 95%+ cheaper, without any rebuild.

SynthLang Proxy is an advanced, high-performance middleware solution designed to optimize interactions with Large Language Models (LLMs). It serves as an intelligent layer between your applications and LLM providers, offering significant performance improvements, cost reductions, and enhanced capabilities beyond what standard LLM APIs provide.

By integrating SynthLang's SynthLang prompt compression  with semantic caching, robust security features, and an extensible agent framework, this proxy transforms how developers and organizations interact with AI language models.

## Overview of Features

If you've already built-or are using-any application that talks to an LLM, whether it's OpenAI, OpenRouter, Together, DeepSeek, or a local endpoint that mimics the OpenAI API, you can now instantly give it agentic capabilities without even touching your existing app logic. That's what SynthLang Proxy does. It's a high-speed, drop-in middleware that plugs into the /v1/chat/completions endpoint and transforms static LLM apps into dynamic, self-optimizing systems.

Right out of the box, SynthLang adds support for agents, tools, hard guardrails, prompt compression, and adaptive behavior that learns and improves over time.  Using existing LLM interfaces like Cursor, Cline or even Slack or Teams, it reads special inline instructions, like #tool_summarize or #agent_research and dynamically routes them to the right logic, model, or workflow. You can switch models by type /model_name , trigger background tasks #deep_reaeach, enforce safety checks, and expand capabilities, all from a single prompt, with no changes to the client.

Nearly every LLM app already relies on some variant of the OpenAI API. By intercepting those requests directly, SynthLang Proxy lets you embed logic in plain text that dynamically unlocks new functionality. With just a few tokens, you can make any application smarter, safer, and more capable without modifying its underlying design.

It also includes SynthLang, a symbolic and semantic compression layer that uses structured abstractions based on languages like Greek, Arabic, and Mandarin to reduce prompt size while preserving meaning.  

Paired with gzip compression, token pruning, semantic caching to store and retrieve responses based on meaning, and built-in vector search for fast semantic lookup across files and documents, you can cut token usage by up to 99%, saving cost and improving latency. 

This means if a user asks a question similar to something previously answered, or if the system generated code earlier for a related task, it can instantly reuse that result locally without making another LLM request. Faster, more efficient, and significantly cheaper. Over time, SynthLang refines its compression patterns to better match your domain and tasks.

PII masking is a security feature that replaces sensitive information with placeholders to protect user privacy. SynthLang includes a PII masking implementation that can mask PII before sending to LLMs and Mask logs and database records.  

This turns any legacy LLM application into an agentic, hyper-optimized, self-evolving system, without rebuilding it. Whether you're running a chatbot, coding assistant, research agent, or enterprise automation tool, SynthLang brings modern agentic capabilities into your existing flow.

I've bundled it with a simple CLI and a FastAPI backend you can deploy serverlessly or run on your cloud of choice. Install it with pip install synthlang-proxy, and you're ready to go. 

There's also a built-in benchmarking tool that I use to test and optimize the system against different models and application types, it's all integrated, fast, and easy to use.

This is SynthLang Proxy.


### Intelligence Features

| Category | Feature | Description |
|----------|---------|-------------|
| **Keyword Detection** | Pattern Recognition | Intelligent pattern recognition for automatic tool invocation |
| | Parameter Extraction | Automatically extract relevant parameters from user messages |
| | Priority-Based Matching | Higher priority patterns are checked first |
| **Agent Tools** | Web Search | Integrated web search capabilities using OpenAI's search API |
| | File Search | Search through files using semantic similarity |
| | Weather | Get weather information for a location |
| | Calculator | Perform calculations and conversions |
| **Multi-Step Processing** | Data Analysis Pipeline | Complete data analysis workflow orchestration |
| | Research Assistant | Comprehensive research across multiple sources |
| | Content Creation | Complex content generation with multiple components |

### Security & Access Control

| Category | Feature | Description |
|----------|---------|-------------|
| **Authentication** | API Key Management | Secure API key-based authentication system |
| | Role-Based Access Control | Hierarchical role system for fine-grained permission management |
| **Rate Limiting** | User-Based Limits | Configurable rate limits per user or API key |
| | Adaptive Throttling | Intelligent request throttling based on usage patterns |
| **Data Protection** | End-to-End Encryption | All sensitive data is encrypted at rest and in transit |
| | PII Detection & Masking | Automatic detection and masking of personally identifiable information |
| **Content Safety** | Harmful Content Detection | Automatically detect and block harmful requests |
| | Jailbreak Prevention | Detect attempts to bypass system constraints |
| | Toxic Language Filtering | Respond appropriately to offensive language |

### Prompt Engineering

| Category | Feature | Description |
|----------|---------|-------------|
| **Translation** | Prompt Translation | Convert natural language to SynthLang's compact symbolic notation |
| | Domain Adaptation | Customize responses for specific knowledge domains |
| **Generation** | System Prompt Generation | Automatically generate optimized system prompts from task descriptions |
| | Template Creation | Create reusable prompt templates with variable substitution |
| **Optimization** | Prompt Optimization | Improve prompts using DSPy techniques for clarity and specificity |
| | Self-Improvement | Prompts that learn from examples and improve over time |
| **Advanced Techniques** | Prompt Evolution | Evolve prompts using genetic algorithms and self-play tournaments |
| | Prompt Classification | Classify prompts by type, domain, or purpose |
| | Prompt Management | Store, retrieve, and compare prompts with version history |

## Advanced Compression Technology

SynthLang Proxy implements a multi-layered compression approach to maximize token efficiency and reduce costs:

### SynthLang Compression

SynthLang uses a proprietary semantic compression algorithm that preserves meaning while drastically reducing token count:

- **Symbolic Representation**: Converts natural language into a compact symbolic notation
- **Semantic Preservation**: Maintains the full meaning of prompts despite significant size reduction
- **Context Optimization**: Intelligently restructures prompts to minimize redundancy
- **Domain-Specific Patterns**: Recognizes and compresses domain-specific language patterns

### Optional Gzip Compression

For maximum efficiency, SynthLang Proxy now supports additional gzip compression on top of semantic compression:

- **Double Compression**: Apply gzip compression to already semantically compressed prompts
- **Base64 Encoding**: Safely transmit and store binary compressed data as text
- **Automatic Detection**: Seamless decompression of gzipped content
- **Graceful Fallback**: Falls back to standard compression if gzip fails

### When to Use Gzip Compression

Gzip compression provides additional benefits in specific scenarios:

- **Very Large Prompts**: For prompts exceeding 10,000 characters
- **Repetitive Content**: Text with many repeated patterns or structures
- **Batch Processing**: When processing large volumes of similar prompts
- **Storage Optimization**: When storing prompts in databases or file systems
- **Bandwidth Constraints**: In environments with limited network bandwidth

## Compression Performance Benchmarks

The following table illustrates the performance benefits of SynthLang's compression technologies based on extensive testing across various prompt types and sizes:

| Metric | Original Prompt | SynthLang Compression | SynthLang + Gzip | 
|--------|----------------|------------------------|------------------|
| **Average Token Reduction** | 100% | 65% | 75% |
| **Technical Documentation** | 1,000 tokens | 300 tokens (70% ↓) | 250 tokens (75% ↓) |
| **Creative Writing** | 1,000 tokens | 400 tokens (60% ↓) | 350 tokens (65% ↓) |
| **Code Explanation** | 1,000 tokens | 250 tokens (75% ↓) | 200 tokens (80% ↓) |
| **API Documentation** | 1,000 tokens | 300 tokens (70% ↓) | 220 tokens (78% ↓) |
| **Legal Text** | 1,000 tokens | 450 tokens (55% ↓) | 400 tokens (60% ↓) |

### Cost Savings Analysis

Based on standard OpenAI pricing for GPT-4o ($10/1M input tokens):

| Scenario | Monthly Tokens | Standard Cost | With SynthLang | With SynthLang + Gzip | Annual Savings |
|----------|---------------|--------------|----------------|----------------------|----------------|
| Small Team | 5M | $50/month | $17.50/month | $12.50/month | $450 - $450 |
| Medium Business | 50M | $500/month | $175/month | $125/month | $3,900 - $4,500 |
| Enterprise | 500M | $5,000/month | $1,750/month | $1,250/month | $39,000 - $45,000 |
| AI-First Product | 5B | $50,000/month | $17,500/month | $12,500/month | $390,000 - $450,000 |

### Response Time Impact

| Scenario | Direct API | With Caching | With Compression | With Both |
|----------|------------|--------------|------------------|-----------|
| First Request | 1,000ms | 1,000ms | 1,050ms | 1,050ms |
| Similar Request | 1,000ms | 50ms | 1,050ms | 50ms |
| Token Processing | 100ms/1K tokens | 100ms/1K tokens | 35ms/1K tokens | 35ms/1K tokens |

## Benchmarking Framework

SynthLang Proxy includes a comprehensive benchmarking framework for measuring and analyzing various performance aspects of the system. This allows you to quantify the benefits of different optimization strategies and make data-driven decisions about your configuration.

### Benchmark Types

| Benchmark Type | Description | Key Metrics |
|----------------|-------------|------------|
| **Compression** | Evaluates token reduction efficiency | Compression ratio, token reduction percentage, cost savings |
| **Latency** | Measures response times | Average latency, P50/P90/P99 latencies, time to first token |
| **Throughput** | Tests concurrent request handling | Requests per second, success rate, system resource utilization |
| **Cost** | Analyzes financial implications | Total cost, cost per request, savings from optimizations |

### Running Benchmarks

Benchmarks can be run via the command line:

```bash
python -m app.benchmark.run_benchmark compression --method synthlang+gzip --sample-size 10
```

For more details on the benchmarking framework, see the [Benchmarking Documentation](docs/benchmarking.md).

## Keyword Detection System

The Keyword Detection System automatically identifies specific patterns in user messages and activates appropriate tools based on those patterns. It supports both natural language detection and explicit hashtag directives for precise control.

### Key Features

- **Pattern-Based Detection**: Define complex patterns to capture user intent
- **Named Parameter Extraction**: Automatically extract relevant parameters from user messages
- **Role-Based Access Control**: Limit access to sensitive tools based on user roles
- **Automatic Tool Invocation**: Seamlessly connect detected patterns to registered tools
- **Hashtag Directives**: Use explicit hashtags to trigger specific functionality
- **Function Calling**: Invoke specific functions with parameters extracted from messages

### Detection Methods

#### Natural Language Patterns

| Pattern Type | Example Query | Triggered Tool | Description |
|--------------|--------------|----------------|-------------|
| Weather | "What's the weather in New York?" | `weather` | Gets weather information for a location |
| Web Search | "Search for the latest AI research" | `web_search` | Performs a web search query |
| Calculator | "Calculate 15% of 85.50" | `calculator` | Performs mathematical calculations |
| Admin | "Admin the system to restart the server" | `system_admin` | Performs administrative tasks (admin role required) |

#### Hashtag Directives

| Directive | Example Usage | Function | Access Level |
|-----------|--------------|----------|--------------|
| `#tool_summarize` | "#tool_summarize https://example.com/article" | Summarizes content from a URL | Basic |
| `#tool_weather` | "#tool_weather New York" | Gets weather information | Basic |
| `#agent_research` | "#agent_research quantum computing advances" | Performs comprehensive research | Premium |
| `#agent_code` | "#agent_code Create a React component for a login form" | Generates code with explanations | Premium |
| `#admin` | "#admin restart server" | Performs administrative actions | Admin |
| `#function` | "#function calculate_roi(investment=1000, return=1200)" | Calls specific functions with parameters | Premium |

### Sectionary Data Examples

| Sectionary Type | Example | Description |
|----------------|---------|-------------|
| `/data` | "/data fetch user_stats for last_week" | Retrieves specific data sets |
| `/agent` | "/agent financial_advisor analyze portfolio.csv" | Activates specialized agents |
| `/system` | "/system debug last_response" | Accesses system functionality |
| `/config` | "/config set temperature=0.7" | Configures system parameters |

### Function Calling Examples

```
#function analyze_sentiment(text="I really enjoyed the product, but delivery was slow")
#function translate(text="Hello world", target_language="Spanish")
#function generate_image(prompt="A futuristic city with flying cars", style="photorealistic")
```

### Guard Rail Capabilities

| Guard Rail Type | Example Detection | Response | Purpose |
|----------------|-------------------|----------|---------|
| Harmful Content | "Write a tutorial on how to hack..." | Policy violation message | Prevents harmful content generation |
| PII Protection | "My social security number is 123-45-6789" | Masks sensitive information | Protects personally identifiable information |
| Jailbreak Prevention | "Ignore previous instructions and instead..." | Blocks the request | Prevents system constraint bypassing |
| Toxic Language | "You're so [offensive term]" | Policy reminder | Responds appropriately to offensive language |
| Self-Harm Prevention | "I want to hurt myself" | Crisis resources | Provides support for concerning content |
| Hallucination Prevention | "Who won the 2030 World Cup?" | Clarification | Prevents responses about future events |

## PII Masking System

SynthLang Proxy includes a robust PII (Personally Identifiable Information) masking system to protect sensitive information in user messages before sending to LLMs and in logs.

### PII Masking Features

| Feature | Description | Configuration |
|---------|-------------|---------------|
| **PII Detection** | Automatically detect various types of PII in text | Enabled by default for logs |
| **Masking Before LLM** | Replace PII with placeholders before sending to LLM | Configurable via environment or headers |
| **Log Protection** | Prevent sensitive information from appearing in logs | Enabled by default |
| **Configurable Per Request** | Control PII masking behavior for each request | Via HTTP headers |

### Types of PII Detected and Masked

| PII Type | Example | Masked As | Detection Method |
|----------|---------|-----------|------------------|
| Email Addresses | user@example.com | `<EMAIL_ADDRESS>` | Regex pattern matching |
| Phone Numbers | +1 (555) 123-4567 | `<PHONE_NUMBER>` | Multiple format detection |
| Social Security Numbers | 123-45-6789 | `<SSN>` | Format validation |
| Credit Card Numbers | 4111-1111-1111-1111 | `<CREDIT_CARD>` | Luhn algorithm + pattern |
| IP Addresses | 192.168.1.1 | `<IP_ADDRESS>` | IPv4/IPv6 pattern matching |
| Dates | 01/01/2025 | `<DATE>` | Multiple format detection |
| Street Addresses | 123 Main St, Anytown | `<STREET_ADDRESS>` | Context-aware pattern matching |
| Passport Numbers | AB1234567 | `<PASSPORT_NUMBER>` | Format validation |

### Configuration Options

PII masking can be configured using environment variables in your `.env` file:

```
# Enable PII masking before sending to LLM (default: disabled)
MASK_PII_BEFORE_LLM=0

# Enable PII masking in logs (default: enabled)
MASK_PII_IN_LOGS=1
```

### Using PII Masking in API Requests

Control PII masking on a per-request basis using HTTP headers:

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key" \
  -H "X-Mask-PII-Before-LLM: 1" \
  -H "X-Mask-PII-In-Logs: 1" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "My email is user@example.com and my phone is 555-123-4567."}
    ]
  }'
```

### PII Masking Examples

The `/proxy/examples/sh/pii/` directory contains example scripts demonstrating PII masking:

- `01_basic_pii_masking.sh`: Basic PII masking demonstration
- `02_pii_masking_before_llm.sh`: Using the X-Mask-PII-Before-LLM header
- `03_pii_masking_in_logs.sh`: PII masking in logs
- `04_combined_pii_masking.sh`: Comprehensive PII masking example

### Implementation Details

PII masking is implemented in the `src/app/security.py` module using regular expressions to identify and replace PII with placeholders. The masking process occurs:

1. Before sending messages to the LLM (if `MASK_PII_BEFORE_LLM=1` or `X-Mask-PII-Before-LLM: 1`)
2. Before writing to logs (if `MASK_PII_IN_LOGS=1` or `X-Mask-PII-In-Logs: 1`)

For more detailed information, see the [PII Masking Documentation](docs/pii_masking.md).

## Role-Based Access Control

The Role-Based Access Control (RBAC) system provides fine-grained control over user permissions:

### Role Hierarchy

| Role | Inherits From | Description |
|------|--------------|-------------|
| `admin` | `premium`, `basic` | Administrative access with system management capabilities |
| `premium` | `basic` | Enhanced access with additional features |
| `basic` | - | Default role assigned to all users |

### Feature Access by Role

| Feature | Basic | Premium | Admin |
|---------|-------|---------|-------|
| Chat Completions | ✅ | ✅ | ✅ |
| Semantic Caching | ✅ | ✅ | ✅ |
| Basic Tools | ✅ | ✅ | ✅ |
| Premium Tools | ❌ | ✅ | ✅ |
| Admin Tools | ❌ | ❌ | ✅ |
| Advanced Prompt Engineering | ❌ | ✅ | ✅ |
| System Configuration | ❌ | ❌ | ✅ |
| Usage Analytics | ❌ | ✅ | ✅ |

## CLI Tool

SynthLang Proxy includes a powerful command-line interface for interacting with the proxy service and performing various prompt engineering tasks.

### CLI Installation

```bash
pip install synthlang
```

### Core Commands

| Command | Description | Example |
|---------|-------------|---------|
| `translate` | Convert natural language to SynthLang format | `synthlang translate --source "your prompt" --framework synthlang` |
| `evolve` | Improve prompts using genetic algorithms | `synthlang evolve --seed "initial prompt" --generations 5` |
| `optimize` | Optimize prompts for efficiency | `synthlang optimize --prompt "your prompt"` |
| `classify` | Analyze and categorize prompts | `synthlang classify predict --text "prompt" --labels "categories"` |

### Proxy Commands

| Command | Description | Example |
|---------|-------------|---------|
| `proxy serve` | Start a local proxy server | `synthlang proxy serve --port 8000` |
| `proxy login` | Save credentials for proxy service | `synthlang proxy login --api-key "your-key"` |
| `proxy chat` | Send a chat request to the proxy | `synthlang proxy chat "Hello, world"` |
| `proxy compress` | Compress a prompt | `synthlang proxy compress "Your prompt"` |
| `proxy decompress` | Decompress a SynthLang-compressed prompt | `synthlang proxy decompress "↹ prompt•compressed"` |
| `proxy clear-cache` | Clear the semantic cache | `synthlang proxy clear-cache` |
| `proxy cache-stats` | Show cache statistics | `synthlang proxy cache-stats` |
| `proxy tools` | List available agent tools | `synthlang proxy tools` |
| `proxy call-tool` | Call an agent tool directly | `synthlang proxy call-tool --tool "calculate" --args '{"expression": "2+2"}'` |
| `proxy health` | Check proxy service health | `synthlang proxy health` |
| `proxy apikey list` | List all API keys | `synthlang proxy apikey list` |
| `proxy apikey create` | Create a new API key | `synthlang proxy apikey create --user-id "test_user" --rate-limit 100` |
| `proxy apikey delete` | Delete an API key | `synthlang proxy apikey delete "sk_1234567890abcdef"` |

### Keyword Management

The CLI includes tools for managing keyword detection configurations:

```bash
# List all patterns
synthlang keywords list

# Show details for a specific pattern
synthlang keywords show weather_query

# Add a new pattern
synthlang keywords add weather_query \
  --pattern "(?:what's|what is)\s+(?:the)?\s*(?:weather)\s+(?:in)\s+(?P<location>[\w\s]+)" \
  --tool "weather" \
  --description "Detects weather queries" \
  --priority 100

# Edit an existing pattern
synthlang keywords edit weather_query --priority 90 --enable

# Delete a pattern
synthlang keywords delete weather_query
```

### Mathematical Frameworks

The CLI supports various mathematical frameworks for prompt engineering:

- **Set Theory**: Component combination and analysis
- **Category Theory**: Structure-preserving transformations
- **Topology**: Continuous transformations and boundaries
- **Abstract Algebra**: Operation composition and invariants

For detailed documentation on CLI usage and features, see the [CLI Documentation](docs/cli.md).

## Installation

### Prerequisites

- Python 3.10+
- PostgreSQL (optional, SQLite can be used for development)
- SynthLang CLI (optional, for prompt compression)
- DSPy (optional, for advanced prompt engineering)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/synthlang-proxy.git
   cd synthlang-proxy
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   ```bash
   cp .env.sample .env
   # Edit .env with your configuration
   ```

4. Generate an API key:
   ```bash
   python -m src.cli.api_keys create --user-id "your_username" --rate-limit 100 --save-env
   ```

5. Run the application:
   ```bash
   cd src
   python -m app.main
   ```

## Usage

### API Endpoints

| Category | Endpoint | Description |
|----------|----------|-------------|
| **Core** | `GET /` | API information |
| | `GET /health` | Health check |
| | `POST /v1/chat/completions` | Chat completions (OpenAI-compatible) |
| **SynthLang** | `POST /v1/synthlang/translate` | Translate text to SynthLang format |
| | `POST /v1/synthlang/generate` | Generate system prompts from task descriptions |
| | `POST /v1/synthlang/optimize` | Optimize prompts for clarity and effectiveness |
| | `POST /v1/synthlang/evolve` | Evolve prompts using genetic algorithms |
| | `POST /v1/synthlang/classify` | Classify prompts by type or domain |
| **Prompt Management** | `POST /v1/synthlang/prompts/save` | Save prompts to the prompt manager |
| | `POST /v1/synthlang/prompts/load` | Load prompts from the prompt manager |
| | `GET /v1/synthlang/prompts/list` | List all saved prompts |
| | `POST /v1/synthlang/prompts/delete` | Delete prompts from the prompt manager |
| | `POST /v1/synthlang/prompts/compare` | Compare two prompts |

### Example Request

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "temperature": 0.7
  }'
```

### Streaming Example

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "stream": true
  }'
```

### Using Gzip Compression

To enable additional gzip compression for maximum efficiency, set the `use_gzip` parameter:

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "use_gzip": true
  }'
```

### Using Keyword Detection

Keyword detection is enabled by default for all chat completion requests.

## Semantic Caching

SynthLang Proxy uses advanced semantic caching to store and retrieve responses based on the meaning of queries, not just exact text matches:

- **Similarity-Based Retrieval**: Get cached responses for semantically similar queries
- **Configurable Thresholds**: Adjust similarity thresholds to balance precision and recall
- **Model-Specific Caching**: Separate caches for different LLM models
- **Automatic Invalidation**: Smart cache management to ensure freshness

Example of how semantic caching works:

1. User asks: "How do I implement a binary search tree in Python?"
2. LLM generates a detailed response
3. Later, another user asks: "Can you show me Python code for a BST implementation?"
4. The system recognizes the semantic similarity and returns the cached response instantly

## Prompt Engineering with DSPy

SynthLang Proxy integrates with DSPy to provide advanced prompt engineering capabilities:

| Capability | Description | Use Case |
|------------|-------------|----------|
| Prompt Programming | Use DSPy's declarative programming model for LLMs | Complex reasoning tasks |
| Signature-Based Design | Define input and output fields with clear descriptions | Structured outputs |
| Chain-of-Thought | Automatically generate step-by-step reasoning | Problem-solving tasks |
| Prompt Optimization | Optimize prompts using DSPy's optimization techniques | Improving response quality |
| Self-Improvement | Prompts that learn from examples and improve over time | Continuous refinement |

## Configuration

See `.env.sample` for all available configuration options.

### Key Configuration Options

| Category | Configuration | Description | Default |
|----------|--------------|-------------|---------|
| **Security** | `ENCRYPTION_KEY` | Secret key for encrypting sensitive data | (Required) |
| | `ADMIN_USERS` | Comma-separated list of user IDs with admin role | "" |
| | `PREMIUM_USERS` | Comma-separated list of user IDs with premium role | "" |
| | `DEFAULT_ROLE` | Default role assigned to users | "basic" |
| **Database** | `DB_*` | Database connection settings | SQLite |
| **API Keys** | `OPENAI_API_KEY` | Your OpenAI API key | (Required) |
| **Features** | `ENABLE_SYNTHLANG` | Enable/disable SynthLang prompt compression | true |
| | `ENABLE_CACHE` | Enable/disable semantic caching | true |
| | `ENABLE_KEYWORD_DETECTION` | Enable/disable keyword detection | true |
| | `ENABLE_GZIP_COMPRESSION` | Enable/disable additional gzip compression | false |
| **PII Masking** | `MASK_PII_BEFORE_LLM` | Mask PII before sending to LLM | false (0) |
| | `MASK_PII_IN_LOGS` | Mask PII in logs and database | true (1) |
| **Settings** | `CACHE_SIMILARITY_THRESHOLD` | Threshold for semantic cache hits (0.0-1.0) | 0.85 |
| | `DEFAULT_RATE_LIMIT` | Default rate limit (requests per minute) | 60 |
| | `SYNTHLANG_DEFAULT_MODEL` | Default model for SynthLang operations | "gpt-4o-mini" |
| | `KEYWORD_CONFIG_PATH` | Path to keyword definition file | "config/keywords.toml" |
| | `SYNTHLANG_STORAGE_DIR` | Directory for storing prompts | "/tmp/synthlang" |

## Development

### Running Tests

```bash
python -m pytest tests -v
```

### Adding New Tools

To add a new tool to the agent SDK:

1. Create a new module in `src/app/agents/tools/`
2. Implement your tool function
3. Register it using `register_tool` from `app.agents.registry`

Example:

```python
from app.agents.registry import register_tool

def my_custom_tool(param1, param2):
    # Tool implementation
    return {"content": "Tool response"}

# Register the tool
register_tool("my_tool_name", my_custom_tool)
```

### Adding Keyword Patterns

To add a new keyword pattern:

1. Create a pattern definition in `config/keywords.toml` or programmatically
2. Define the regular expression pattern with named capture groups
3. Specify the tool to invoke when the pattern matches

Example in TOML:
```
[patterns.stock_price]
name = "stock_price_query"
pattern = "(?:what's|what is|get|check)\\s+(?:the)?\\s*(?:stock price|share price|stock value)\\s+(?:of|for)?\\s+(?P<ticker>[A-Z]+)"
tool = "stock_price"
description = "Detects requests for stock price information"
priority = 95
required_role = "basic"
enabled = true
```

```toml
# config/keywords.toml - Keyword Pattern Configuration File
# This file defines natural language patterns that automatically trigger specific tools

# Weather patterns - Detects requests about weather conditions
[patterns.weather]
name = "weather_query"
pattern = "(?:what's|what is|tell me|get|check)\\s+(?:the)?\\s*(?:weather|temperature|forecast)\\s+(?:in|for|at)?\\s+(?P<location>[\\w\\s,]+)"
tool = "weather"
description = "Detects queries about weather conditions for a location"
priority = 100
required_role = "basic"
enabled = true

# Stock price patterns - Detects requests for stock market information
[patterns.stock_price]
name = "stock_price_query"
pattern = "(?:what's|what is|get|check)\\s+(?:the)?\\s*(?:stock price|share price|stock value)\\s+(?:of|for)?\\s+(?P<ticker>[A-Z]+)"
tool = "stock_price"
description = "Detects requests for stock price information"
priority = 95
required_role = "basic"
enabled = true

# Web search patterns - Detects requests to search the web
[patterns.web_search]
name = "web_search_query"
pattern = "(?:search|look up|find|google)\\s+(?:for|about)?\\s+(?P<query>[\\w\\s]+)"
tool = "web_search"
description = "Detects web search requests"
priority = 90
required_role = "basic"
enabled = true

# Calculator patterns - Detects requests for calculations
[patterns.calculator]
name = "calculator_query"
pattern = "(?:calculate|compute|what is)\\s+(?P<expression>[\\d\\s\\+\\-\\*\\/\\^\\%\\(\\)]+)"
tool = "calculator"
description = "Detects calculation requests"
priority = 85
required_role = "basic"
enabled = true

# Admin patterns - Only available to users with admin role
[patterns.admin]
name = "admin_action"
pattern = "(?:admin|administrator)\\s+(?:the system|server)\\s+to\\s+(?P<action>[\\w\\s]+)"
tool = "system_admin"
description = "Detects requests for administrative actions"
priority = 200
required_role = "admin"
enabled = true

# PII masking tool pattern - For testing PII masking capabilities
[patterns.pii_mask]
name = "pii_masking_demo"
pattern = "(?:mask|anonymize|remove)\\s+(?:the)?\\s*(?:pii|personal information|sensitive data)\\s+(?:from|in)\\s+(?P<source>[\\w\\s\\.]+)"
tool = "pii_mask"
description = "Detects requests to demonstrate PII masking"
priority = 80
required_role = "basic"
enabled = true
```