# Gremllm

Instead of getting gremlins OUT of your code, we're going to put them IN.

Gremllm provides AI-powered dynamic objects that can evolve their behavior at runtime through LLM calls.

## Installation

```bash
pip install gremllm
```

## Quick Start

```python
import gremllm

counter = gremllm.new('counter')
counter.value = 1
counter.increment()
print(f"counter: {counter.value}")
```

The magic happens when you call methods on Gremllm objects - they use AI to decide what code to execute!

## Features

- Dynamic method generation through LLM calls
- Safe code evaluation in controlled contexts
- Emergent behavior as objects evolve
- Perfect for creative coding and AI experiments

## Warning

This is an art project exploring AI and code. Use responsibly and never in production systems.