Instead of getting gremlins OUT of your code, we're going to put them IN.

The idea is like inside-out LLM tool calling. You make an instance of Gremllm and all (or most) of the methods you invoke on it are run through an LLM to decide what code to evaluate. So here is an example:

```python
import Gremllm

counter = Gremllm.new('counter')
counter.value = 1
counter.increment()
println(f"counter: {counter.value}")
```

So here the Gremllm.new creates a new Gremllm instance which knows that it is a "counter". When we call `counter.value = 1` it should:

* Invoke the assignment operator of the Gremllm
* which should invoke some LLM and ask it what to do
* which should respond (maybe using structured JSON) with a python string to eval
* and then we eval the string in the context of the Gremllm counter context
* so it can access local instance variables, call other methods (including Gremllm methods), etc
* might have to use some debugging-tool type tricks to set the right context/scope for the eval
* heck it could define a method that is no longer dynamic, that would be fine. Sort of de-gremllm itself if it wants
* return the result of the eval
* the caller only sees what it passed in to the gremllm and what it got back out

Some notes
* the LLM call can be an API call, but could also be local

