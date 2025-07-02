#!/usr/bin/env python3
"""
Example usage of Gremllm - testing the counter example from idea.md
"""

import gremllm


def main():
    print("=== Gremllm Counter Example ===")
    print("This demonstrates gremllm-powered dynamic objects")
    print("Make sure you have configured your LLM (run: llm install llm-openai and llm keys set openai)\n")

    try:
        # Create a new counter - the gremllm will implement its behavior
        # You can specify different models: gremllm.new("counter", model="claude-3-5-sonnet-20241022")
        counter = gremllm.new("counter")
        print(f"✓ Created counter: {counter}")

        # Set initial value - gremllm decides how to handle assignment
        print("\n→ Setting counter.value = 5")
        counter.value = 5
        print(f"✓ Value set: {counter}")

        # Get the value - gremllm decides how to handle access
        print(f"\n→ Getting counter.value: {counter.value}")

        # Call increment method - gremllm will create this method dynamically
        print("\n→ Calling counter.increment() - gremllm will implement this!")
        result = counter.increment()
        print(f"✓ Increment result: {result}")
        print(f"✓ New counter value: {counter.value}")

        # Try incrementing by a specific amount
        print("\n→ Calling counter.increment(3)")
        result2 = counter.increment(3)
        print(f"✓ Increment(3) result: {result2}")
        print(f"✓ New counter value: {counter.value}")

        print(f"\n→ counter.as_roman_numeral(): {counter.as_roman_numeral()}")

        # Try some other operations the gremllm might implement
        print("\n→ Let's see what else this gremllm counter can do...")
        print(f"→ counter.reset(): {counter.reset()}")
        print(f"✓ Counter after reset: {counter.value}")

        print(f"\n→ counter.description: {counter.description}")

        print(f"\n🎉 Final counter state: {counter}")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
