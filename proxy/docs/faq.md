# Frequently Asked Questions

This document addresses common questions about SynthLang Proxy.

## General Questions

### What is SynthLang Proxy?

SynthLang Proxy is an advanced middleware solution that sits between your applications and Large Language Model (LLM) providers. It adds powerful features like prompt compression, semantic caching, agent tools, and keyword detection without requiring any changes to your existing applications.

### How does SynthLang Proxy work?

SynthLang Proxy acts as a drop-in replacement for OpenAI's API. It intercepts API calls to the `/v1/chat/completions` endpoint (and other endpoints), applies optimizations like compression and caching, and then forwards the request to the actual LLM provider. The response follows the same path in reverse, being processed by SynthLang Proxy before being returned to your application.

### What are the main benefits of using SynthLang Proxy?

The main benefits include:

- **Cost Reduction**: Reduce token usage by up to 75% through compression and caching
- **Performance Improvement**: Lower latency and higher throughput
- **Enhanced Capabilities**: Add agentic behaviors, tools, and custom functionality
- **No Client Changes**: Works with existing applications without modifications
- **Compatibility**: Compatible with the OpenAI API format

### Which LLM providers are supported?

SynthLang Proxy primarily supports OpenAI's API, but it can be extended to support other providers that use a similar API format. The core proxy is designed to be provider-agnostic, with adapter modules for specific providers.

### Is SynthLang Proxy open source?

Yes, SynthLang Proxy is open source and released under the MIT License. You can find the source code on GitHub.

## Installation and Configuration

### What are the system requirements for SynthLang Proxy?

The minimum requirements are:

- Python 3.10 or higher
- 2GB RAM (4GB+ recommended)
- 200MB disk space plus additional space for database and logs
- Outbound HTTPS access to API providers

### Can I run SynthLang Proxy in a Docker container?

Yes, SynthLang Proxy includes a Dockerfile and docker-compose.yml for containerized deployment. See the [Deployment Guide](deployment.md) for details.

### How do I configure SynthLang Proxy?

Configuration is primarily done through environment variables or a `.env` file. See the [Configuration section](user_guide.md#configuration) in the User Guide for details.

### Can I run SynthLang Proxy on serverless platforms?

Yes, SynthLang Proxy can be deployed on serverless platforms like AWS Lambda, Google Cloud Functions, or Azure Functions. See the [Serverless Deployment section](deployment.md#serverless-deployment) in the Deployment Guide for details.

### How do I upgrade SynthLang Proxy to a new version?

If installed via pip:

```bash
pip install --upgrade synthlang-proxy
```

If installed from source:

```bash
git pull
pip install -e .
```

Remember to check the changelog for any breaking changes or migration steps.

## Features and Usage

### How does SynthLang compression work?

SynthLang compression uses a combination of semantic compression techniques to reduce token count while preserving meaning. It converts natural language into a compact symbolic notation, removes redundancy, and optimizes structure. For detailed information, see the [Compression System documentation](compression_system.md).

### How much token reduction can I expect?

Typical token reduction ranges from 40% to 75%, depending on the content type:

- Technical documentation: 70-80% reduction
- Code explanation: 75-80% reduction
- Creative writing: 60-65% reduction
- General text: 65-70% reduction

### How does semantic caching work?

Semantic caching stores responses based on the semantic meaning of requests, not just exact text matching. When a new request comes in, it's compared to previously cached requests using vector embeddings and cosine similarity. If a similar request is found above the similarity threshold, the cached response is returned. See the [Semantic Caching documentation](semantic_caching.md) for details.

### What is the Keyword Detection System?

The Keyword Detection System automatically identifies patterns in user messages and activates appropriate tools based on those patterns. This allows SynthLang Proxy to provide more responsive and context-aware interactions. For example, if a user asks "What's the weather in London?", the system can automatically trigger a weather tool without requiring an explicit command. See the [Keyword Detection documentation](keyword_detection.md) for details.

### What agent tools are available out of the box?

SynthLang Proxy includes several built-in tools:

- Web Search
- Weather
- Calculator
- File Search
- Data Analysis
- Code Generator
- Document Summarizer

You can also create custom tools to extend functionality. See the [Agent Framework and Tools documentation](agents_tools.md) for details.

### How do I create custom agent tools?

You can create custom tools by:

1. Creating a new Python function that follows the tool function interface
2. Registering it using the `register_tool` function
3. Optionally adding a keyword pattern for automatic detection

See the [Creating Custom Tools section](agents_tools.md#creating-custom-tools) in the Agent Framework documentation for details.

### What is Role-Based Access Control (RBAC)?

RBAC allows you to control which users can access specific features, tools, and resources within SynthLang Proxy. It uses a hierarchical role system where higher-level roles inherit permissions from lower-level roles. See the [Role-Based Access Control documentation](role_based_access_control.md) for details.

## Performance and Scaling

### How many requests can SynthLang Proxy handle?

The throughput depends on your hardware, configuration, and usage patterns. On a typical modern server with 4 cores and 8GB RAM, SynthLang Proxy can handle hundreds of requests per minute. With semantic caching enabled, throughput can be significantly higher for similar requests.

### How does SynthLang Proxy impact latency?

SynthLang Proxy adds a small processing overhead (typically 5-20ms) to requests. However, the benefits of semantic caching can dramatically reduce overall latency for similar requests, as cached responses are returned almost instantly without calling the LLM API.

### Can SynthLang Proxy be horizontally scaled?

Yes, SynthLang Proxy can be horizontally scaled by running multiple instances behind a load balancer. For distributed deployments, you'll need to configure a shared cache backend (like Redis) and a shared database. See the [High-Availability Deployment section](deployment.md#high-availability-deployment) in the Deployment Guide.

### How do I monitor SynthLang Proxy performance?

SynthLang Proxy exposes metrics via a `/metrics` endpoint in Prometheus format. You can use Prometheus and Grafana to collect and visualize these metrics. The proxy also logs performance information that can be analyzed with your preferred logging tools.

### What database options are supported?

SynthLang Proxy supports:

- PostgreSQL (recommended for production)
- SQLite (suitable for development/testing)

The database is primarily used for persistent storage of cache entries, user data, and configuration.

## Troubleshooting

### Why am I getting "Unauthorized" errors?

This typically means your API key is invalid or missing. Check that:

1. You've set the `OPENAI_API_KEY` environment variable correctly
2. You're passing a valid API key in the `Authorization` header
3. Your API key has the necessary permissions

### Why isn't semantic caching working?

If you're not seeing cache hits:

1. Check that caching is enabled (`ENABLE_CACHE=1`)
2. Verify the similarity threshold (`CACHE_SIMILARITY_THRESHOLD`) isn't too high
3. Make sure your requests are semantically similar enough
4. Check cache statistics (`synthlang proxy cache-stats`) to confirm the cache is being used

### Why isn't compression reducing tokens as expected?

Compression effectiveness varies depending on content:

1. Very short prompts may not compress well
2. Very unstructured text may not compress well
3. Check that compression is enabled (`USE_SYNTHLANG=1`)
4. Try different compression levels or domain-specific compression

### How do I fix database connection errors?

If you're seeing database connection errors:

1. Verify your database is running
2. Check the connection URL in your `.env` file
3. Ensure the database user has the necessary permissions
4. If using PostgreSQL, check that the `asyncpg` package is installed
5. If using SQLite, check that the database directory is writable

### Why aren't my custom tools being detected?

If your custom tools aren't being detected:

1. Verify the tool is properly registered
2. Check your keyword pattern regex for errors
3. Ensure the pattern is enabled
4. Try using the explicit hashtag directive (`#tool_name`)
5. Check tool execution logs for errors

### How do I debug a failing API request?

To debug failing requests:

1. Enable debug logging (`LOG_LEVEL=DEBUG`)
2. Check the proxy log file for detailed error messages
3. Use the health check endpoint (`/health`) to verify the service is running
4. Try curl or Postman to send a basic request and check the raw response

### Why am I seeing high memory usage?

High memory usage could be due to:

1. Large cache size (adjust `CACHE_MAX_ITEMS`)
2. Many concurrent requests (adjust worker configuration)
3. Memory leaks in custom tool implementations
4. Vector index memory usage (adjust embedding configuration)

## Security

### Is my data secure?

SynthLang Proxy implements several security measures:

1. API key authentication
2. Role-based access control
3. Input validation
4. Rate limiting
5. PII masking (optional)
6. Encryption of sensitive data

### Does SynthLang Proxy store user messages?

By default, SynthLang Proxy only stores messages in the semantic cache, which you can configure or disable. No permanent message storage is done unless you explicitly configure database persistence.

### How are API keys managed?

You can use a fixed API key set in the environment variables, or implement custom API key logic. The proxy authenticates requests using API keys but doesn't handle key generation or rotation by default.

### Can I use SynthLang Proxy with sensitive data?

Yes, but you should:

1. Enable PII masking (`MASK_PII_BEFORE_LLM=1`)
2. Configure secure storage with proper encryption
3. Set appropriate user roles and permissions
4. Consider deploying in a private network or VPC
5. Follow your organization's data handling policies

## Billing and Usage

### How much can SynthLang Proxy reduce my API costs?

Typical cost reductions range from 40% to 75%, depending on your usage patterns:

- Compression typically reduces token usage by 40-75%
- Semantic caching can further reduce costs by serving cached responses
- Combined, these features can reduce API costs by 60-90% for high-volume applications

### How is token usage calculated?

Token usage is calculated by:

1. Counting the tokens in the original request
2. Counting the tokens in the compressed request (if compression is enabled)
3. Recording the difference as savings
4. Tracking cache hits (which avoid token usage entirely)

The proxy provides usage metrics to help you track these savings.

### Does SynthLang Proxy have usage limits?

The open source version has no built-in limits. Your usage is only constrained by your hardware resources and the rate limits of your LLM provider.

## Integration

### Can I use SynthLang Proxy with my existing application?

Yes, SynthLang Proxy is designed as a drop-in replacement for the OpenAI API. In most cases, you just need to change the API endpoint URL in your application to point to SynthLang Proxy instead of directly to OpenAI.

### Which frameworks and languages are supported?

Any framework or language that can make HTTP requests can use SynthLang Proxy. The service provides a standard REST API that can be accessed from any programming language.

### Can I use SynthLang Proxy with Cursor, ChatGPT, or other LLM applications?

Yes, if the application allows you to configure a custom API endpoint, you can point it to your SynthLang Proxy instance. Some applications may require additional configuration or custom integration.

### How do I integrate SynthLang Proxy with my CI/CD pipeline?

You can include SynthLang Proxy in your CI/CD pipeline by:

1. Adding it as a service in your pipeline configuration
2. Setting the appropriate environment variables
3. Configuring your application to use the proxy endpoint
4. Including proxy metrics in your monitoring

### Can I use SynthLang Proxy with Azure OpenAI?

Yes, you can configure SynthLang Proxy to use Azure OpenAI as the LLM provider. You'll need to set the appropriate environment variables for Azure OpenAI authentication and endpoints.

## Getting Help

### Where can I get support for SynthLang Proxy?

You can get support through:

1. GitHub Issues for bug reports and feature requests
2. Community forums for questions and discussions
3. Documentation for reference information
4. Example repositories for implementation guidance

### How do I report a bug?

To report a bug:

1. Check existing issues on GitHub to see if it's already reported
2. Create a new issue with detailed information about the bug
3. Include steps to reproduce, expected behavior, and actual behavior
4. Attach logs, error messages, and environment details if possible

### How do I request a new feature?

To request a new feature:

1. Check existing issues and discussions to see if it's already requested
2. Create a new issue with a clear description of the feature
3. Explain the use case and benefits of the feature
4. Provide examples of how the feature would be used

### How do I contribute to SynthLang Proxy?

Contributions are welcome! See the [Contributing section](development.md#contributing) in the Development Guide for details on:

1. Setting up a development environment
2. Making code changes
3. Running tests
4. Submitting pull requests