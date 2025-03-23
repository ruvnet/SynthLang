# Changelog

All notable changes to the SynthLang CLI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-03-23

### Added
- Proxy service integration
  - Local proxy server with `proxy serve` command
  - API client for remote proxy services
  - Authentication with `proxy login` and `proxy logout` commands
  - Chat completion with `proxy chat` command
- Advanced prompt compression
  - SynthLang compression algorithm
  - Optional gzip compression
  - Compression metrics and statistics
- Semantic caching
  - Automatic caching of API responses
  - Cache management commands
  - Cache statistics
- Agent SDK and tool registry
  - Built-in tools for common tasks
  - Tool discovery and execution from CLI
  - Extensible tool registry
- Proxy integration with existing commands
  - `--use-proxy` flag for translate and optimize commands
  - Fallback to local implementation when proxy unavailable
- Documentation
  - Proxy integration tutorial
  - Updated README with proxy commands
  - Command help text

### Changed
- Updated dependencies to support proxy functionality
- Improved error handling and logging
- Enhanced CLI structure with command groups

## [0.1.0] - 2024-01-01

### Added
- Initial release of SynthLang CLI
- Core DSPy module implementation
- Framework translation functionality
  - Support for translating between different frameworks
  - Detailed translation explanations
- System prompt generation
  - Task-based prompt generation
  - Rationale for generated prompts
- Configuration management
  - Environment variable support
  - JSON configuration files
  - Command-line configuration interface
- Logging system
  - Multiple log levels
  - File and console logging
  - Rich formatting for console output
- Command-line interface
  - `init` command for configuration setup
  - `translate` command for code translation
  - `generate` command for prompt generation
  - `optimize` command placeholder for future optimization features
  - `config` command group for managing settings
- Documentation
  - Usage guide
  - Development guide
  - API documentation
- Testing
  - Unit tests for all components
  - Integration tests for key features
  - Test fixtures and utilities

### Changed
- Set default model to gpt-4o-mini

### Fixed
- None (initial release)

## Version History

- 0.2.0 (2025-03-23)
  - Added proxy integration and advanced features
- 0.1.0 (2024-01-01)
  - Initial release

## Versioning Policy

SynthLang CLI follows semantic versioning:
- MAJOR version for incompatible API changes
- MINOR version for new functionality in a backward compatible manner
- PATCH version for backward compatible bug fixes
