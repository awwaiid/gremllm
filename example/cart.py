#!/usr/bin/env python3
"""
Test shopping cart with JSON functionality
"""

import gremllm


def main():
    print("=== Testing Shopping Cart with JSON ===")

    try:
        # Create a shopping cart - you can use any model supported by llm library
        # Examples: model="claude-3-5-sonnet-20241022", model="gpt-4", etc.
        cart = gremllm.new("shopping_cart")
        print(f"✓ Created cart: {cart}")

        # Add some items
        print("\n→ Adding items to cart")
        cart.add_item("apple", 1.50)
        cart.add_item("banana", 0.75)
        cart.add_item("orange", 2.00)

        # Try to get contents as JSON (this should work now)
        print("\n→ Getting cart contents as JSON:")
        json_contents = cart.contents_as_json()
        print(f"✓ JSON contents: {json_contents}")

        # Calculate total
        print("\n→ Calculating total:")
        total = cart.calculate_total()
        print(f"✓ Total: ${total}")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
