# SynthLang Proxy

Synthlang Proxy turns any existing LLM app (OpenAi v1/Endpoint) or Coder (Cursor etc) into an agentic, hyper-optimized, self-evolving system and it's 95%+ cheaper, without any rebuild.

If you’ve already built-or are using-any application that talks to an LLM, whether it’s OpenAI, OpenRouter, Together, DeepSeek, or a local endpoint that mimics the OpenAI API, you can now instantly give it agentic capabilities without even touching your existing app logic. 

That’s what SynthLang Proxy does. It’s a high-speed, drop-in middleware that plugs into the /v1/chat/completions endpoint and transforms static LLM apps into dynamic, self-optimizing systems.

Right out of the box, SynthLang adds support for agents, tools, hard guardrails, prompt compression, and adaptive behavior that learns and improves over time. Using existing LLM interfaces like Cursor, Cline or even Slack or Teams, it reads special inline instructions, like #tool_summarize or #agent_research and dynamically routes them to the right logic, model, or workflow. You can switch models by type /model_name , trigger background tasks #deep_reaeach, enforce safety checks, and expand capabilities, all from a single prompt, with no changes to the client.

Nearly every LLM app already relies on some variant of the OpenAI API. By intercepting those requests directly, SynthLang Proxy lets you embed logic in plain text that dynamically unlocks new functionality. With just a few tokens, you can make any application smarter, safer, and more capable without modifying its underlying design.

It also includes SynthLang, a symbolic and semantic compression layer that uses structured abstractions based on languages like Greek, Arabic, and Mandarin to reduce prompt size while preserving meaning.  

Paired with gzip compression, token pruning, semantic caching to store and retrieve responses based on meaning, and built-in vector search for fast semantic lookup across files and documents, you can cut token usage by up to 99%, saving cost and improving latency. 

This means if a user asks a question similar to something previously answered, or if the system generated code earlier for a related task, it can instantly reuse that result locally without making another LLM request. Faster, more efficient, and significantly cheaper. Over time, SynthLang refines its compression patterns to better match your domain and tasks.

This turns any legacy LLM application into an **agentic, hyper-optimized, self-evolving system, **without rebuilding it. Whether you’re running a chatbot, coding assistant, research agent, or enterprise automation tool, SynthLang brings modern agentic capabilities into your existing flow.

I’ve bundled it with a simple CLI and a FastAPI backend you can deploy serverlessly or run on your cloud of choice. Install it with pip install spark-proxy, and you’re ready to go.  There’s also a built-in benchmarking tool that I use to test and optimize the system against different models and application types, it’s all integrated, fast, and easy to use.

This is SynthLang Proxy.

## Introduction

SynthLang Proxy is an advanced, high-performance middleware solution designed to optimize interactions with Large Language Models (LLMs). It serves as an intelligent layer between your applications and LLM providers, offering significant performance improvements, cost reductions, and enhanced capabilities beyond what standard LLM APIs provide.

By integrating SynthLang's proprietary prompt compression technology with semantic caching, robust security features, and an extensible agent framework, this proxy transforms how developers and organizations interact with AI language models.

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

### Keyword Management

The CLI includes tools for managing keyword detection configurations:

```bash
# List all patterns
synthlang keywords list

# Show details for a specific pattern
synthlang keywords show weather_query

# Add a new pattern
synthlang keywords add weather_query \
  --pattern "(?:what's|what is)\\s+(?:the)?\\s*(?:weather)\\s+(?:in)\\s+(?P<location>[\\w\\s]+)" \
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
