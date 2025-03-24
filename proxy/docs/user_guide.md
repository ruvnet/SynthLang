# User Guide

This guide provides detailed information on how to use SynthLang Proxy effectively.

## Table of Contents

[toc]

## Core Features

### Prompt Compression

SynthLang Proxy significantly reduces token usage and costs through its advanced prompt compression techniques.

#### Overview of SynthLang Compression

SynthLang compression is a proprietary semantic compression algorithm that preserves the meaning of prompts while drastically reducing the token count. It uses symbolic representation, semantic preservation, context optimization, and domain-specific patterns to achieve high compression ratios.

#### How to Enable and Use Compression

Prompt compression is enabled by default in SynthLang Proxy. You can control it using the `USE_SYNTHLANG` environment variable in your `.env` file. Set `USE_SYNTHLANG=1` to enable or `USE_SYNTHLANG=0` to disable.

When enabled, SynthLang Proxy automatically compresses incoming prompts before sending them to the LLM provider and decompresses responses before returning them to the client. This process is transparent to your application.

#### Compression Methods and Options

SynthLang Proxy offers multiple compression methods:

- **SynthLang Compression**: Semantic compression using symbolic notation.
- **SynthLang + Gzip**: Combines SynthLang compression with gzip for even higher compression ratios. Enable gzip compression by setting `use_gzip: true` in your request payload.

#### Performance Benefits and Cost Savings

SynthLang compression offers significant performance benefits:

- **Reduced Token Usage**: Up to 75% token reduction, leading to substantial cost savings.
- **Improved Latency**: Smaller prompts result in faster processing times and lower latency.
- **Increased Throughput**: Reduced token processing overhead allows for higher request throughput.

See the [Benchmarking Documentation](benchmarking.md) for detailed performance metrics and cost savings analysis.

### Semantic Caching

Semantic caching in SynthLang Proxy drastically improves response times and reduces costs by storing and reusing responses to semantically similar queries.

#### Overview of Semantic Caching

SynthLang Proxy's semantic cache stores LLM responses based on the semantic meaning of the requests, not just exact text matches. This allows the proxy to return cached responses for queries that are similar but not identical to previous requests.

#### How Caching Works in SynthLang Proxy

1.  **Request Analysis**: When a request is received, SynthLang Proxy analyzes its semantic meaning.
2.  **Cache Lookup**: The proxy searches the semantic cache for semantically similar previous requests.
3.  **Cache Hit**: If a similar request is found (cache hit), the cached response is returned immediately, bypassing the LLM call.
4.  **Cache Miss**: If no similar request is found (cache miss), the request is forwarded to the LLM, and the response is stored in the cache for future use.

#### Configuration Options for Caching

Semantic caching can be configured using environment variables in your `.env` file:

- `ENABLE_CACHE`: Enable or disable semantic caching (default: `1` for enabled, `0` for disabled).
- `CACHE_SIMILARITY_THRESHOLD`:  Adjust the similarity threshold (0.0-1.0) for cache hits. A higher threshold (e.g., 0.95) requires very high similarity, while a lower threshold (e.g., 0.85) allows for more flexible matching.
- `CACHE_MAX_ITEMS`: Set the maximum number of items to store in the cache.

#### Cache Invalidation and Management

SynthLang Proxy automatically manages the cache, evicting older or less frequently used items when the cache reaches its maximum capacity. You can also manually clear the cache using the CLI command:

```bash
synthlang proxy clear-cache
```

#### Monitoring Cache Performance

To monitor the performance of the semantic cache, you can use the CLI command:

```bash
synthlang proxy cache-stats
```

This command provides statistics about cache hits, misses, and cache size, helping you optimize your caching configuration.

### PII Masking

SynthLang Proxy includes a robust PII (Personally Identifiable Information) masking system to protect sensitive information in user messages before sending to LLMs and in logs.

#### Overview of PII Masking

The PII masking system automatically detects and replaces sensitive information with placeholders, ensuring that personal data is not exposed to LLMs or stored in logs. This helps maintain privacy and comply with data protection regulations.

#### Types of PII Detected and Masked

SynthLang Proxy can detect and mask various types of PII:

- **Email addresses**: `user@example.com` → `<EMAIL_ADDRESS>`
- **Phone numbers**: `+1 (888) 555-1234` → `<PHONE_NUMBER>`
- **Social Security Numbers**: `123-45-6789` → `<SSN>`
- **Credit card numbers**: `4111-1111-1111-1111` → `<CREDIT_CARD>`
- **IP addresses**: `192.168.1.1` → `<IP_ADDRESS>`
- **Dates**: `01/01/2025` → `<DATE>`
- **Street addresses**: `123 Main St, Anytown, CA` → `<STREET_ADDRESS>`
- **Passport numbers**: `AB1234567` → `<PASSPORT_NUMBER>`

#### Configuration Options for PII Masking

PII masking can be configured using environment variables in your `.env` file:

- `MASK_PII_BEFORE_LLM`: Enable or disable PII masking before sending to LLMs (default: `0` for disabled, `1` for enabled).
- `MASK_PII_IN_LOGS`: Enable or disable PII masking in logs (default: `1` for enabled, `0` for disabled).

#### Using PII Masking in API Requests

You can control PII masking on a per-request basis using HTTP headers:

- `X-Mask-PII-Before-LLM`: Set to `1` to enable PII masking before sending to LLM, or `0` to disable.
- `X-Mask-PII-In-Logs`: Set to `1` to enable PII masking in logs, or `0` to disable.

Example API request with PII masking headers:

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

#### Implementation Details

PII masking is implemented in the `src/app/security.py` module using regular expressions to identify and replace PII with placeholders. The masking process occurs:

1. Before sending messages to the LLM (if `MASK_PII_BEFORE_LLM=1` or `X-Mask-PII-Before-LLM: 1`)
2. Before writing to logs (if `MASK_PII_IN_LOGS=1` or `X-Mask-PII-In-Logs: 1`)

#### Example and Testing

You can find examples of PII masking in the `/proxy/examples/sh/pii/` directory:

- `01_basic_pii_masking.sh`: Demonstrates basic PII masking in text
- `02_pii_masking_before_llm.sh`: Shows how to use the `X-Mask-PII-Before-LLM` header
- `03_pii_masking_in_logs.sh`: Illustrates PII masking in logs
- `04_combined_pii_masking.sh`: Demonstrates a combination of PII masking techniques

For more detailed information, see the [PII Masking Documentation](pii_masking.md).

### Agent Framework

SynthLang Proxy transforms static LLM applications into dynamic, agentic systems with its built-in agent framework.

#### Introduction to Agentic Capabilities

The agent framework allows you to extend your LLM applications with agentic capabilities, enabling them to perform actions, interact with tools, and make decisions based on user requests. SynthLang Proxy supports tools, function calling, and multi-step workflows, all triggered dynamically from user prompts.

#### Built-in Tools and Agents

SynthLang Proxy includes several built-in tools and agents:

- **Web Search**: Uses OpenAI's search capability to perform web searches.
- **File Search**: Searches through files using semantic similarity.
- **Weather**: Gets weather information for a location.
- **Calculator**: Performs calculations and conversions.
- **Data Analysis Pipeline**: Orchestrates a complete data analysis workflow (premium feature).
- **Research Assistant**: Conducts comprehensive research across multiple sources (premium feature).
- **Content Creation Agent**: Generates complex content with multiple components (premium feature).

You can list available tools using the CLI command:

```bash
synthlang proxy tools
```

#### How to Use Tools in Prompts

Tools can be invoked in prompts using special directives, hashtags, or natural language patterns.

- **Hashtag Directives**: Use hashtags like `#tool_summarize` or `#tool_weather` to explicitly trigger tools. For example:

  ```
  #tool_weather London
  ```

- **Natural Language Patterns**: The Keyword Detection System automatically identifies patterns in user messages and invokes relevant tools. For example, asking "What's the weather in New York?" will trigger the `weather` tool.

- **Function Calling**: Use `#function` directives to call specific functions with parameters. For example:

  ```
  #function calculate_roi(investment=1000, return=1200)
  ```

#### Extending with Custom Tools

You can easily extend SynthLang Proxy with custom tools by implementing tool functions and registering them with the agent registry. See the [Development Documentation](development.md) for details on creating and registering custom tools.

#### Agentic Workflows and Examples

Agentic workflows enable complex, multi-step processes to be orchestrated from user prompts. For example, the `Data Analysis Pipeline` agent can be triggered by a user request like:

```
Analyze the sales data from Q1 2025 and generate a forecast
```

This will initiate a multi-step workflow involving data loading, cleaning, analysis, and reporting, all handled by the `data_analysis_agent` tool.

### Keyword Detection System

The Keyword Detection System in SynthLang Proxy intelligently identifies patterns in user messages and automatically activates appropriate tools.

#### Overview of Keyword Detection

The Keyword Detection System acts as middleware, analyzing user messages against a registry of keyword patterns. When a pattern is matched, the system extracts parameters and invokes the corresponding tool, enabling context-aware interactions without explicit tool commands.

#### How to Configure Keyword Patterns

Keyword patterns are configured in TOML files or programmatically. Each pattern definition includes:

- **Name**: Unique identifier for the pattern.
- **Pattern**: Regular expression to match user messages. Use named capture groups to extract parameters.
- **Tool**: Name of the tool to invoke.
- **Description**: Human-readable description.
- **Required Role**: (Optional) Role required to use the pattern.
- **Priority**: Pattern priority (higher values checked first).
- **Enabled**: Whether the pattern is active.

Example TOML configuration:

```toml
[patterns.weather_query]
name = "weather_query"
pattern = "(?:what's|what is|how's|how is)\\s+(?:the)?\\s*(?:weather|temperature)\\s+(?:like)?\\s*(?:in|at|near)?\\s+(?P<location>[\\w\\s]+)"
tool = "weather"
description = "Detects weather queries"
priority = 100
enabled = true
```

You can manage keyword patterns using the CLI `keywords.py` tool. See the [CLI Documentation](cli.md) for details.

#### Role-Based Access Control for Keywords

Keyword patterns can be restricted to specific user roles. The `required_role` parameter in the pattern configuration allows you to specify the role needed to trigger the pattern. This ensures that sensitive tools are only accessible to authorized users.

#### Using Keywords for Tool Invocation

When a user message matches a keyword pattern and the user has the required role (if specified), the Keyword Detection System automatically invokes the associated tool. Parameters extracted from the message using named capture groups in the regex pattern are passed to the tool function.

#### Guard Rail Implementation with Keywords

The Keyword Detection System can be used to implement guard rails for content moderation, PII detection, jailbreak prevention, and safety measures. By defining patterns for harmful content, toxic language, or self-harm indicators, you can automatically trigger tools that enforce policies, filter content, or provide crisis support.

Example guard rail pattern:

```toml
[patterns.harmful_content]
name = "harmful_content_detector"
pattern = "(?i)(?:how to|tutorial|guide|instructions for)\\s+(?:hack|steal|break into|illegally access)\\s+(?P<target>.+)"
tool = "content_moderator"
description = "Detects requests for harmful content"
priority = 200
required_role = "basic"
enabled = true
```

### Role-Based Access Control (RBAC)

SynthLang Proxy implements Role-Based Access Control (RBAC) to provide flexible and secure user permission management.

#### Introduction to RBAC

RBAC enables fine-grained control over user access to features, tools, and resources within SynthLang Proxy. It uses roles, which are collections of permissions assigned to users. The system includes a role hierarchy where higher-level roles inherit permissions from lower-level roles.

Default roles:

- **basic**: Default role for all users.
- **premium**: Enhanced access with additional features.
- **admin**: Administrative access for system management.

Role Hierarchy:

```
admin → premium → basic
```

#### Role Hierarchy and Permissions

The role hierarchy defines inheritance:

- `admin` users inherit `premium` and `basic` permissions.
- `premium` users inherit `basic` permissions.
- `basic` role is the foundation for all users.

Permissions are implicitly defined by role assignment. For example, premium role might grant access to advanced tools, while admin role grants access to system configuration endpoints.

#### Configuration of Roles and Users

RBAC is configured using environment variables:

- `ADMIN_USERS`: Comma-separated list of user IDs with admin role.
- `PREMIUM_USERS`: Comma-separated list of premium user IDs.
- `DEFAULT_ROLE`: Default role for new users (default: "basic").

Example:

```
ADMIN_USERS=user1,user2
PREMIUM_USERS=user3,user4,user5
DEFAULT_ROLE=basic
```

Roles are also defined programmatically in the system:

```python
ROLE_HIERARCHY = {
    "admin": ["premium"],
    "premium": ["basic"],
    "basic": []
}

DEFAULT_ROLES = ["basic"]
```

#### Integrating RBAC with Tools and Keywords

RBAC is integrated with:

- **Tool Registry**: Restrict tool access using the `@require_role` decorator.
- **Keyword Detection System**: Restrict pattern matching using the `required_role` parameter in keyword definitions.
- **API Endpoints**: Protect API endpoints by checking user roles before granting access.

#### Security Considerations for RBAC

- **Principle of Least Privilege**: Assign roles with minimal necessary permissions.
- **Admin Role Restriction**: Limit admin roles to trusted users.
- **Regular Audits**: Audit role assignments periodically.
- **Role Verification**: Always verify roles server-side before granting access.
- **Secure Role Storage**: For production, consider database-backed role storage.

## Advanced Features

### Benchmarking Framework

SynthLang Proxy includes a comprehensive benchmarking framework to measure and analyze system performance.

#### Overview of the Benchmarking Framework

The benchmarking framework allows you to evaluate various performance aspects of SynthLang Proxy, including compression efficiency, latency, throughput, and cost. It helps you understand the impact of different configurations and optimizations.

#### Benchmark Types and Metrics

The framework supports several benchmark types:

- **Compression Benchmark**: Evaluates token reduction and cost savings from SynthLang's compression.
  - **Metrics**: Compression ratio, token reduction percentage, cost savings percentage, compression time.
- **Latency Benchmark**: Measures response times and time-to-first-token.
  - **Metrics**: Average latency, percentile latencies (P50, P90, P99), time to first token (TTFT), processing time.
- **Throughput Benchmark**: Tests the system's capacity to handle concurrent requests.
  - **Metrics**: Requests per second, total requests, successful requests, failed requests, average response time, system resource utilization.
- **Cost Benchmark**: Analyzes the financial impact of optimization strategies.
  - **Metrics**: Total cost, cost per request, savings from compression and caching, token usage statistics.

#### Running Benchmarks from CLI and Programmatically

Benchmarks can be run from the command line using the `run_benchmark.py` script:

```bash
python -m app.benchmark.run_benchmark [benchmark_type] [options]
```

Available benchmark types: `compression`, `latency`, `throughput`, `cost`.

See [Benchmarking Documentation](benchmarking.md) for CLI options and examples.

Benchmarks can also be run programmatically using the `default_runner` API.

```python
from app.benchmark import default_runner
from app.benchmark.scenarios.compression import CompressionBenchmark

benchmark = CompressionBenchmark("compression")
default_runner.register_scenario(benchmark)
parameters = {
    "compression_method": "synthlang",
    "model": "gpt-4o",
    "text_type": "general",
    "sample_size": 5,
}
result = default_runner.run_benchmark("compression", parameters)
print(result.metrics)
```

#### Analyzing Benchmark Results

Benchmark results are saved as JSON files in the `benchmark_results` directory. Each result file includes:

- Benchmark configuration
- Measured metrics
- Timestamp and unique identifier
- Raw data points

You can analyze these results to understand performance and optimize your SynthLang Proxy setup.

#### Creating Custom Benchmarks

You can create custom benchmark scenarios by extending the `BenchmarkScenario` class. This allows you to tailor benchmarks to your specific use cases and performance requirements. See [Benchmarking Documentation](benchmarking.md) for details on creating custom benchmarks.

### SynthLang Integration

SynthLang Proxy integrates the core functionality of SynthLang to provide advanced prompt engineering capabilities directly within the proxy service.

#### Deep Dive into SynthLang Integration

The integration allows you to leverage SynthLang's prompt translation, generation, optimization, evolution, and management features through the proxy API. This modular integration uses existing SynthLang core modules and exposes them via FastAPI endpoints.

#### Using SynthLang API Endpoints

SynthLang integration provides the following API endpoints under `/v1/synthlang`:

- `POST /v1/synthlang/translate`: Translate natural language prompts to SynthLang format.
- `POST /v1/synthlang/generate`: Generate system prompts from task descriptions.
- `POST /v1/synthlang/optimize`: Optimize prompts using DSPy techniques.
- `POST /v1/synthlang/evolve`: Evolve prompts using genetic algorithms.
- `POST /v1/synthlang/classify`: Classify prompts using DSPy.
- `POST /v1/synthlang/prompts/save`: Save prompts to the prompt manager.
- `POST /v1/synthlang/prompts/load`: Load prompts from the prompt manager.
- `GET /v1/synthlang/prompts/list`: List all saved prompts.
- `POST /v1/synthlang/prompts/delete`: Delete prompts from the prompt manager.
- `POST /v1/synthlang/prompts/compare`: Compare two prompts.

#### Prompt Translation, Generation, Optimization, and Evolution

- **Prompt Translation**: Convert natural language to SynthLang symbolic notation using the `/v1/synthlang/translate` endpoint.
- **System Prompt Generation**: Generate optimized system prompts from task descriptions using `/v1/synthlang/generate`.
- **Prompt Optimization**: Improve prompt efficiency and clarity using DSPy with `/v1/synthlang/optimize`.
- **Prompt Evolution**: Evolve prompts using genetic algorithms for better performance with `/v1/synthlang/evolve`.

See the [API Documentation](api.md) for request and response formats for these endpoints.

#### Prompt Management Features

SynthLang integration includes prompt management features:

- **Save Prompts**: Use `/v1/synthlang/prompts/save` to store prompts with names and metadata.
- **Load Prompts**: Retrieve saved prompts using `/v1/synthlang/prompts/load` by name.
- **List Prompts**: Get a list of all saved prompts with `/v1/synthlang/prompts/list`.
- **Delete Prompts**: Remove prompts using `/v1/synthlang/prompts/delete` by name.
- **Compare Prompts**: Compare two prompts and analyze differences using `/v1/synthlang/prompts/compare`.

These features help you organize, manage, and version your prompts effectively.

### CLI Tool

SynthLang Proxy includes a powerful Command-Line Interface (CLI) for interacting with the proxy and performing prompt engineering tasks.

#### Detailed CLI Command Reference

The CLI tool `synthlang` provides various commands and subcommands:

**Core Commands**:

- `translate`: Translate natural language to SynthLang format.
- `evolve`: Improve prompts using genetic algorithms.
- `optimize`: Optimize prompts for efficiency.
- `classify`: Analyze and categorize prompts.

**Proxy Commands**:

- `proxy serve`: Start a local proxy server.
- `proxy login`: Save credentials for the proxy service.
- `proxy logout`: Remove saved credentials.
- `proxy chat`: Send a chat request to the proxy.
- `proxy compress`: Compress a prompt using SynthLang.
- `proxy decompress`: Decompress a SynthLang-compressed prompt.
- `proxy clear-cache`: Clear the semantic cache.
- `proxy cache-stats`: Show cache statistics.
- `proxy tools`: List available agent tools.
- `proxy call-tool`: Call an agent tool directly.
- `proxy health`: Check proxy service health.

**Keyword Management Commands** (using `keywords.py`):

- `list`: List all keyword patterns.
- `show`: Show details for a specific pattern.
- `add`: Add a new keyword pattern.
- `edit`: Edit an existing pattern.
- `delete`: Delete a pattern.
- `import`: Import patterns from a configuration file.
- `export`: Export patterns to a configuration file.
- `create-default`: Create a default configuration.
- `settings`: Show current keyword detection settings.
- `update-settings`: Update keyword detection settings.

See [CLI Documentation](cli.md) for detailed command options and usage.

#### Usage Examples for all Commands

Refer to the [CLI Documentation](cli.md) for detailed usage examples for each command, including options and parameters. Examples cover prompt translation, optimization, proxy server management, cache operations, tool invocation, and keyword pattern management.

#### Configuration Options via CLI

The CLI tool can be configured via:

- **Environment Variables**:  Set environment variables like `OPENAI_API_KEY`, `SYNTHLANG_PROXY_URL`, etc.
- **Configuration File**: Create a `.env` file in your working directory or home directory to set configuration variables.
- **Command-Line Arguments**: Some commands accept command-line arguments for specific configurations (e.g., `--port` for `proxy serve`).

#### Keyword Management via CLI

The `keywords.py` CLI tool provides comprehensive keyword management capabilities:

- **Listing, Showing, Adding, Editing, Deleting Patterns**: Manage keyword patterns using `list`, `show`, `add`, `edit`, and `delete` commands.
- **Importing/Exporting Configurations**: Import and export keyword configurations using `import` and `export` commands.
- **Managing Settings**: View and update keyword detection settings using `settings` and `update-settings` commands.

See [CLI Documentation](cli.md) for detailed information on keyword management commands and options.

## Configuration

SynthLang Proxy can be configured through environment variables, configuration files, and dynamic settings.

### Environment Variables

Environment variables are the primary way to configure SynthLang Proxy. Key environment variables include:

- **Server Configuration**:
    - `PORT`: Port for the proxy server (default: `8000`).
    - `HOST`: Host address to bind to (default: `0.0.0.0`).
    - `DEBUG`: Enable debug mode (default: `false`).
- **Security**:
    - `ENCRYPTION_KEY`: Encryption key for sensitive data (required).
    - `ADMIN_USERS`: Comma-separated list of admin user IDs.
    - `PREMIUM_USERS`: Comma-separated list of premium user IDs.
    - `DEFAULT_ROLE`: Default user role (default: `basic`).
- **Database**:
    - `DATABASE_URL`: PostgreSQL connection URL (required for PostgreSQL).
    - `USE_SQLITE`: Enable SQLite (set to `1` to enable, default: `0`).
    - `SQLITE_PATH`: Path to SQLite database file.
    - `DEBUG_SQL`: Enable debug SQL logging (default: `0`).
- **Rate Limiting**:
    - `DEFAULT_RATE_LIMIT_QPM`: Default requests per minute limit (default: `60`).
    - `PREMIUM_RATE_LIMIT`: Rate limit for premium users (default: `120`).
- **SynthLang Integration**:
    - `USE_SYNTHLANG`: Enable SynthLang compression (default: `1`).
- **PII Masking**:
    - `MASK_PII_BEFORE_LLM`: Mask PII before sending to LLM (default: `0`).
    - `MASK_PII_IN_LOGS`: Mask PII in logs and database (default: `1`).
- **LLM Provider**:
    - `OPENAI_API_KEY`: OpenAI API key (required).
    - `DEFAULT_MODEL`: Default LLM model (default: `gpt-4o`).
    - `LLM_TIMEOUT`: Timeout for LLM API calls (default: `30`).
- **Semantic Cache**:
    - `ENABLE_CACHE`: Enable semantic cache (default: `1`).
    - `CACHE_SIMILARITY_THRESHOLD`: Cache similarity threshold (default: `0.95`).
    - `CACHE_MAX_ITEMS`: Maximum cache items (default: `1000`).
- **Logging**:
    - `LOG_LEVEL`: Logging level (default: `INFO`).
    - `LOG_FILE`: Log file path (default: `proxy.log`).
- **Keyword Detection**:
    - `ENABLE_KEYWORD_DETECTION`: Enable keyword detection (default: `true`).
    - `KEYWORD_DETECTION_THRESHOLD`: Keyword detection threshold (default: `0.7`).
    - `KEYWORD_CONFIG_PATH`: Path to keyword configuration file (default: `config/keywords.toml`).
- **SynthLang Core**:
    - `SYNTHLANG_FEATURES_ENABLED`: Enable SynthLang features (default: `true`).
    - `SYNTHLANG_DEFAULT_MODEL`: Default model for SynthLang operations (default: `gpt-4o-mini`).
    - `SYNTHLANG_STORAGE_DIR`: Directory for storing prompts (default: `/tmp/synthlang`).


See `.env.sample` for a template configuration file.

### Configuration Files

SynthLang Proxy uses configuration files for keyword patterns and other settings. 

- **`.env` File**:  Store environment variables in a `.env` file in the proxy root directory or home directory. This file is automatically loaded by the application.
- **`config/keywords.toml`**: Configure keyword detection patterns in the `keywords.toml` file. This file defines patterns, tools, roles, and settings for the Keyword Detection System.

### Dynamic Configuration

Some settings can be dynamically configured at runtime, such as:

- **Rate Limits**: Rate limits can be adjusted dynamically based on usage patterns or user roles.
- **Cache Settings**: Cache parameters like `CACHE_SIMILARITY_THRESHOLD` and `CACHE_MAX_ITEMS` can be modified programmatically.
- **Keyword Patterns**: Keyword patterns can be added, updated, or removed at runtime using the CLI or API.

Dynamic configuration allows for flexible adaptation to changing requirements and conditions without restarting the proxy server.
