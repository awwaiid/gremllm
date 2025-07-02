# gremllm

A slight upgrade to the Gremlins in your code, we hereby present GREMLLM. This utility class can be used for a variety of purposes. Uhm. Also please don't use this and if you do please tell me because WOW. Or maybe don't tell me. Or do.

## Installation

    pip install gremllm

## Usage

```python
import gremllm

# Be sure to tell your gremllm what sort of thing it is
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

Basic counter (see [example/counter.py](example/counter.py)):
```python
counter = gremllm.new('counter')
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
# Remind me to not shop at your store
cart = gremllm.new('shopping_cart')
cart.add_item('apple', 1.50)
cart.add_item('banana', 0.75)
total = cart.calculate_total()
print(f"Cart contents: {cart.contents_as_json()}")
print(f"Cart total: {total}")
cart.clear()
```

## Other notes

OMG THIS ACTUALLY WORKS

