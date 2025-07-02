#!/usr/bin/env python3
"""
Example usage of Gremllm - testing the counter example from idea.md
"""

import gremllm


def main():
    print("=== Gremllm Counter Example ===")
    print("This demonstrates AI-powered dynamic objects using OpenAI")
    print("Make sure you have OPENAI_API_KEY in your .env file\n")

    try:
        # Create a new counter - the AI will implement its behavior
        counter = gremllm.new("counter")
        print(f"✓ Created counter: {counter}")

        # Set initial value - AI decides how to handle assignment
        print("\n→ Setting counter.value = 5")
        counter.value = 5
        print(f"✓ Value set: {counter}")

        # Get the value - AI decides how to handle access
        print(f"\n→ Getting counter.value: {counter.value}")

        # Call increment method - AI will create this method dynamically
        print("\n→ Calling counter.increment() - AI will implement this!")
        result = counter.increment()
        print(f"✓ Increment result: {result}")
        print(f"✓ New counter value: {counter.value}")

        # Try incrementing by a specific amount
        print("\n→ Calling counter.increment(3)")
        result2 = counter.increment(3)
        print(f"✓ Increment(3) result: {result2}")
        print(f"✓ New counter value: {counter.value}")

        # Try some other operations the AI might implement
        print("\n→ Let's see what else this AI counter can do...")
        print(f"→ counter.reset(): {counter.reset()}")
        print(f"✓ Counter after reset: {counter.value}")

        print(f"\n→ counter.description: {counter.description}")

        print(f"\n🎉 Final counter state: {counter}")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure you have OPENAI_API_KEY set in your .env file")


if __name__ == "__main__":
    main()
