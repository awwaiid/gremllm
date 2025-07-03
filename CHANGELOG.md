# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-07-03

### Added
- **Wet Mode**: Create immersive experiences where method calls return gremllm objects instead of plain values
- **Verbose Mode**: Debug and inspect generated code with `verbose=True` flag
- **Wet Inheritance**: Child objects automatically inherit `wet` and `verbose` settings from parents
- **Dynamic __repr__**: Objects generate their own contextual string representations via LLM
- Support for multiple LLM providers through Datasette LLM library integration
- **Pythonic Constructor**: Use `Gremllm('identity')` instead of `gremllm.new()`
- Structured JSON output enforcement for consistent LLM responses
- Enhanced error handling for missing library imports
- Library usage guidance (only import common libraries: json, datetime, math, etc.)
- Swimming pool simulator example demonstrating wet mode
- Example output documentation files

### Changed
- **BREAKING**: Constructor changed from `gremllm.new('identity')` to `Gremllm('identity')`
- **BREAKING**: Import changed from `import gremllm` to `from gremllm import Gremllm`
- **BREAKING**: Replaced `llm_provider` parameter with `model` parameter
- Default model changed to `gpt-4o-mini` via Datasette LLM library
- Simplified architecture by removing custom LLM provider abstraction layer
- Updated dependency from `requests` to `llm>=0.12.0`
- Improved prompt engineering with clear wet mode instructions
- Enhanced JSON response parsing with brace cleanup

### Removed
- **BREAKING**: Removed `gremllm.new()` function - use `Gremllm()` constructor directly
- **BREAKING**: Removed `gremllm/llm.py` and custom `LLMProvider` classes
- **BREAKING**: Removed `llm_provider="openai"` parameter
- Removed direct `requests` dependency

### Fixed
- Fixed unmatched brace syntax errors in generated code
- Improved error handling for import failures in generated code
- Better fallback behavior when LLM responses are malformed
- Enhanced __repr__ method stability during object initialization
- Robust JSON response parsing with automatic cleanup

## [0.1.0] - 2025-07-03

### Added
- Initial release of gremllm - "inside-out LLM tool calling"
- Core `Gremllm` class with dynamic method and attribute handling
- `SmartAccessor` for universal method/attribute access
- OpenAI API integration for code generation
- Dynamic code execution in object context
- Basic counter and shopping cart examples
- Package structure with PyPI deployment support
- MIT license
- Basic documentation and usage examples

### Features
- Create dynamic objects: `gremllm.new('counter')`
- LLM-powered method calls: `counter.increment()`
- Dynamic attribute access: `counter.value`
- Persistent object context via `_context` dictionary
- Fallback error handling for graceful degradation