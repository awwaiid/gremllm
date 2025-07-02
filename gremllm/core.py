import json
from typing import Any

import llm


class SmartAccessor:
    """A universal accessor that can be called as a method or used as an attribute."""

    def __init__(self, gremllm_obj, name: str):
        self._gremllm = gremllm_obj
        self._name = name

    def __call__(self, *args, **kwargs):
        """Handle method calls."""
        return self._gremllm._handle_dynamic_access("call", self._name, *args, **kwargs)

    def __str__(self):
        """Handle attribute access via string conversion."""
        return str(self._gremllm._handle_dynamic_access("get", self._name))

    def __repr__(self):
        """Handle attribute access via repr."""
        return str(self._gremllm._handle_dynamic_access("get", self._name))


class Gremllm:
    """
    A dynamic object that uses uh... the sum of human knowledge... to determine behavior at runtime.

    Instead of predefined methods, Gremllm objects ask an LLM what to do
    when methods are called or attributes are accessed.
    """

    def __init__(self, identity: str, model: str = "gpt-4o-mini", **kwargs):
        # Use object.__setattr__ to avoid triggering our custom __setattr__
        object.__setattr__(self, "_identity", identity)
        object.__setattr__(self, "_model", llm.get_model(model))
        object.__setattr__(self, "_context", {})

    def __getattr__(self, name: str) -> Any:
        """Handle attribute access dynamically."""
        if name.startswith("_"):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

        # Return a smart accessor that can handle both method calls and attribute access
        return SmartAccessor(self, name)

    def __setattr__(self, name: str, value: Any) -> None:
        """Handle attribute assignment dynamically through LLM."""
        if name.startswith("_"):
            object.__setattr__(self, name, value)
            return

        # Ask LLM what to do with this assignment
        self._handle_dynamic_access("set", name, value)

    def __call__(self, *args, **kwargs):
        """Make the object itself callable."""
        return self._handle_dynamic_access("call", "__call__", *args, **kwargs)

    def _handle_dynamic_access(self, operation: str, name: str, *args, **kwargs) -> Any:
        """
        Handle dynamic operations by asking the LLM what to do.

        Args:
            operation: 'get', 'set', or 'call'
            name: attribute/method name
            *args, **kwargs: arguments for the operation
        """
        try:
            # Build system and user prompts
            system_prompt = self._build_system_prompt()
            user_prompt = self._build_user_prompt(operation, name, args, kwargs)

            # Get response from LLM using llm library
            response = self._model.prompt(user_prompt, system=system_prompt)

            # Parse and execute the code
            code = self._parse_response(response.text())
            result = self._execute_code(code, name, *args, **kwargs)
            return result

        except Exception as e:
            # Fallback behavior
            if operation == "set":
                self._context[name] = args[0] if args else kwargs
                return None
            elif operation == "get":
                return f"<Gremlin says: Error accessing {name}: {str(e)}>"
            else:
                return f"<Gremlin says: Error in {name}: {str(e)}>"

    def _build_system_prompt(self) -> str:
        """Build the system prompt for the LLM."""
        return f"""You are a helpful AI assistant living inside a Python object called '{self._identity}'.
Someone is interacting with you and you need to respond by generating Python code that will be eval'd in your context.

You have access to 'self' (the object) and can modify self._context to store data.

Rules:
- Always respond with valid JSON: {{"code": "your_python_code_here"}}
- Implement exactly what the user expects - be helpful and predictable
- You can access and modify _context to store persistent data
- Make the object behave naturally as a {self._identity} would"""

    def _build_user_prompt(self, operation: str, name: str, args: tuple, kwargs: dict) -> str:
        """Build the user prompt based on the operation."""
        current_context = dict(self._context)

        if operation == "get":
            action_desc = f"Someone is trying to access your '{name}' attribute"
        elif operation == "set":
            action_desc = f"Someone is trying to set your '{name}' attribute to {args[0] if args else 'something'}"
        elif operation == "call":
            action_desc = f"Someone just called your '{name}' method with args {args} and kwargs {kwargs}"
        else:
            action_desc = f"Someone is doing a '{operation}' operation on '{name}'"

        return f"""{action_desc}.

Your current memory (self._context): {current_context}

What Python code should be executed? Remember:
- You're a {self._identity}, so implement appropriate behavior
- Store persistent data in _context
- Use 'result' variable for what you want to return
- Just execute the operation directly
- You can import any Python libraries you need (json, datetime, math, etc.)

For method calls like 'increment', just do the operation:
```python
_context['value'] += 1
result = _context['value']
```

For method calls that need libraries:
```python
import json
result = json.dumps(_context.get('data', {{}}))
```

For attribute access like 'value', just return the value:
```python
result = _context.get('value', 0)
```"""

    def _parse_response(self, response_text: str) -> str:
        """Parse the LLM response to extract the code."""
        try:
            # Try to parse as JSON first
            data = json.loads(response_text)
            return data.get("code", "")
        except json.JSONDecodeError:
            # If not JSON, assume the entire response is code
            return response_text

    def _execute_code(self, code: str, method_name: str, *args, **kwargs) -> Any:
        """
        Execute LLM-generated code in the instance context.
        """
        # Create a namespace that gives the AI direct access to instance internals
        # Similar to IPython embed - the AI can access all instance attributes directly
        namespace = self.__dict__.copy()
        namespace.update(
            {
                "args": args,
                "kwargs": kwargs,
                "self": self,
            }
        )

        # Execute the code - AI has full access to instance state
        exec(code, globals(), namespace)

        # Return the result
        return namespace.get("result", None)

    def __repr__(self) -> str:
        return f"<Gremllm({self._identity}) context={list(self._context.keys())}>"
