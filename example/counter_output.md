# Counter Example Output

```
=== Gremllm Counter Example ===
This demonstrates gremllm-powered dynamic objects
Make sure you have configured your LLM (run: llm install llm-openai and llm keys set openai)

✓ Created counter: <Gremlin says: Error executing code: name '__repr__' is not defined>

→ Setting counter.value = 5
✓ Value set: 5

→ Getting counter.value: 5

→ Calling counter.increment() - gremllm will implement this!
✓ Increment result: 6
✓ New counter value: 6

→ Calling counter.increment(3)
✓ Increment(3) result: 9
✓ New counter value: 9

→ counter.as_roman_numeral(): None

→ Let's see what else this gremllm counter can do...
→ counter.reset(): 0
✓ Counter after reset: 0

→ counter.description: 1

🎉 Final counter state: 1
```
