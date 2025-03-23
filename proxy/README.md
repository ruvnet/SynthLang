# SynthLang Proxy

Turns out MCPs aren't the best way to do it.

If you've already built—or are using—any application that talks to an LLM, whether it's OpenAI, OpenRouter, Together, DeepSeek, or a local endpoint that mimics the OpenAI API, you can now instantly give it agentic capabilities without touching your existing app logic. That's what SynthLang Proxy does. It's a high-speed, drop-in middleware that plugs into the /v1/chat/completions endpoint and transforms static LLM apps into dynamic, self-optimizing systems.

Right out of the box, SynthLang adds support for agents, tools, hard guardrails, prompt compression, and self-learning behavior. It reads special inline instructions—like #tool_summarize or #agent_research—and dynamically routes them to the right logic, model, or workflow. You can switch models, trigger background tasks, enforce safety checks, and expand capabilities—all from a single prompt, with no changes to the client.

It also includes SynthLang, a symbolic compression layer that uses structured abstractions based on ancient languages like Greek, Arabic, and Mandarin to reduce prompt size. Paired with gzip and token pruning, you can cut token usage by up to 99%, saving cost and improving latency. Over time, SynthLang learns from how it's used, optimizing its behavior to better match each app or use case.

This turns any legacy LLM application into an agentic, hyper-optimized, self-evolving system—without rebuilding it. Whether you're running a chatbot, coding assistant, research agent, or enterprise automation tool, SynthLang brings modern agentic capabilities into your existing flow.

I've bundled it with a simple CLI and a FastAPI backend you can deploy serverlessly or run on your cloud of choice. Install it with pip install spark-proxy, and you're ready to go. There's also a built-in benchmarking tool for testing and tuning performance across different models and application types—it's all integrated, fast, and easy to use.

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
