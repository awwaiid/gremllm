# gremllm

A slight upgrade to the Gremlins in your code, we hereby present GREMLLM. This utility class can be used for a variety of purposes. Uhm. Also please don't use this and if you do please tell me because WOW. Or maybe don't tell me. Or do.

## Installation

    pip install gremllm

## Usage

```python
from gremllm import Gremllm

# Be sure to tell your gremllm what sort of thing it is
counter = Gremllm('counter')
counter.value = 5
counter.increment()
print(counter.value)  # 6?
print(counter.to_roman_numerals()) # VI?
```

Every method call and attribute access goes through a gremllm to decide what code to execute.

## Key Features

- **Dynamic Behavior**: Objects implement methods and properties on-the-fly using LLM reasoning
- **Wet Mode**: Method calls return living gremllm objects instead of plain values for infinite chaining
- **Verbose Mode**: See exactly what code the LLM generates with `verbose=True`
- **Multi-Model Support**: Use OpenAI, Claude, Gemini, or local models via the `llm` library
- **Inheritance**: Child objects automatically inherit `wet` and `verbose` settings
- **Smart Error Handling**: Graceful fallbacks when libraries aren't available or code fails

## Configuration

Configure your preferred LLM using the `llm` library:

```bash
# For OpenAI (default)
llm keys set openai

# For Claude
pip install llm-claude-3
llm keys set claude

# For local models
pip install llm-ollama
```

You can also specify which model to use when creating a gremllm:

```python
from gremllm import Gremllm

# Use default model (gpt-4o-mini)
counter = Gremllm('counter')

# Use specific OpenAI model
counter = Gremllm('counter', model='gpt-4o')

# Use Claude
counter = Gremllm('counter', model='claude-3-5-sonnet-20241022')

# Use local model via Ollama
counter = Gremllm('counter', model='llama2')
```

## Examples

Basic counter (see [example/counter.py](example/counter.py)):
```python
from gremllm import Gremllm

counter = Gremllm('counter')
counter.value = 0
counter.increment()
counter.increment(5)
counter.add_seventeen()
print(counter.current_value)
print(counter.value_in_hex)
counter.reset()
```

Shopping cart (see [example/cart.py](example/cart.py)):
```python
from gremllm import Gremllm

# Remind me to not shop at your store
cart = Gremllm('shopping_cart')
cart.add_item('apple', 1.50)
cart.add_item('banana', 0.75)
total = cart.calculate_total()
print(f"Cart contents: {cart.contents_as_json()}")
print(f"Cart total: {total}")
cart.clear()
```

## Wet Mode

Wet mode creates an immersive experience where method calls return gremllm objects instead of plain values, allowing infinite chaining and interaction:

```python
from gremllm import Gremllm

# Normal mode returns plain values
counter = Gremllm('counter')
result = counter.increment()  # Returns 1 (plain int)

# Wet mode returns living gremllm objects  
wet_counter = Gremllm('counter', wet=True)
result = wet_counter.increment()  # Returns a gremllm number object
doubled = result.double()  # Can call methods on the result!
squared = doubled.square()  # Keep chaining forever!
```

Swimming pool simulator demonstrating wet mode (see [example/wet_pool.py](example/wet_pool.py)):
```python
from gremllm import Gremllm

# Everything stays "wet" and alive in wet mode!
pool = Gremllm('swimming_pool', wet=True)
splash = pool.cannonball()  # Returns a living splash object
ripples = splash.create_ripples()  # Splash creates living ripples
fish = ripples.scare_fish()  # Ripples interact with fish
# Infinite emergent behavior!
```

## Verbose Mode

Debug and understand gremllm behavior by seeing the generated code:

```python
from gremllm import Gremllm

# Enable verbose mode to see generated code
counter = Gremllm('counter', verbose=True)
result = counter.increment()

# Output shows:
# [GREMLLM counter.increment] Generated code:
# ==================================================
# _context['value'] = _context.get('value', 0) + 1
# result = _context['value']
# ==================================================
```

## Other notes

OMG THIS ACTUALLY WORKS

## Further Reading

For background on the concept of "gremlins" in code, see: [Gremlins Three Rules: An Evolutionary Analysis](https://medium.com/@Naturalish/gremlins-three-rules-an-evolutionary-analysis-de4c4fae2785)

