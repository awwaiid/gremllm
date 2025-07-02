# gremllm

A slight upgrade to the Gremlins in your code, we hereby present GREMLLM. This utility class can be used for a variety of purposes. Uhm. Also please don't use this and if you do please tell me because WOW. Or maybe don't tell me. Or do.

## Installation

    pip install gremllm

## Usage

```python
import gremllm

counter = gremllm.new('counter')
counter.value = 5
counter.increment()
print(counter.value)  # 6?
print(counter.to_roman_numerals()) # VI?
```

Every method call and attribute access goes through a gremllm to decide what code to execute.

## Configuration

Set `OPENAI_API_KEY` in environment or `.env` file.

## Examples

Basic counter:
```python
counter = gremllm.new('counter')
counter.value = 0
counter.increment()
counter.increment(5)
counter.reset()
```

Shopping cart:
```python
cart = gremllm.new('shopping_cart')
cart.add_item('apple', 1.50)
cart.add_item('banana', 0.75)
total = cart.calculate_total()
cart.clear()
```

## Dependencies

- requests
- python-dotenv
