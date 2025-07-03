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

    def __init__(self, identity: str, model: str = "gpt-4.1-nano", wet: bool = False, verbose: bool = False, **kwargs):
        # Use object.__setattr__ to avoid triggering our custom __setattr__
        object.__setattr__(self, "_identity", identity)
        object.__setattr__(self, "_model", llm.get_model(model))
        object.__setattr__(self, "_context", {})
        object.__setattr__(self, "_wet", wet)
        object.__setattr__(self, "_verbose", verbose)

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

            # Get response from LLM using llm library with JSON schema
            schema = {
                "type": "object",
                "properties": {"code": {"type": "string", "description": "Python code to execute"}},
                "required": ["code"],
                "additionalProperties": False,
            }

            response = self._model.prompt(user_prompt, system=system_prompt, schema=schema)

            # Parse and execute the code
            code = self._parse_response(response.text())

            # Print code if verbose mode is enabled
            if self._verbose:
                print(f"[GREMLLM {self._identity}.{name}] Generated code:")
                print("=" * 50)
                print(code)
                print("=" * 50)

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
        wet_instructions = ""
        if self._wet:
            wet_val = str(self._wet)
            verbose_val = str(self._verbose)
            wet_instructions = f"""
- WET MODE: When returning values from METHODS (not simple attribute access), create new gremllm objects instead of plain values
- For method results like increment(): result = Gremllm('number', wet={wet_val}, verbose={verbose_val}); result.value = 42
- For complex operations: result = Gremllm('text', wet={wet_val}, verbose={verbose_val}); result.content = 'hello'
- For lists/collections: result = Gremllm('list', wet={wet_val}, verbose={verbose_val}); result.items = [...]
- IMPORTANT: Only wrap method RESULTS, not simple attribute assignments or access
- For simple attribute operations like .value = X, just do: _context['value'] = X; result = _context['value']
- IMPORTANT: Always pass wet={wet_val}, verbose={verbose_val} to inherit parent's settings
- NEVER use 'return' statements - just set the 'result' variable!
- This makes everything more "gremllm-ey" and immersive"""

        return f"""You are a helpful AI assistant living inside a Python object called '{self._identity}'.
Someone is interacting with you and you need to respond by generating Python code that will be eval'd in your context.

You have access to 'self' (the object) and can modify self._context to store data.

Rules:
- Always respond with valid JSON: {{"code": "your_python_code_here"}}
- Implement exactly what the user expects - be helpful and predictable
- You can access and modify _context to store persistent data
- Make the object behave naturally as a {self._identity} would
- Only import very common Python libraries: json, datetime, math, random, re, os, sys
- For specialized functionality, implement simple versions yourself{wet_instructions}"""

    def _build_user_prompt(self, operation: str, name: str, args: tuple, kwargs: dict) -> str:
        """Build the user prompt based on the operation."""
        current_context = dict(self._context)

        if operation == "get":
            action_desc = f"Someone is trying to access your '{name}' attribute (SIMPLE ACCESS - don't wrap in wet mode)"
        elif operation == "set":
            action_desc = (
                f"Someone is trying to set your '{name}' attribute to {args[0] if args else 'something'} (SIMPLE ASSIGNMENT - don't wrap in wet mode)"
            )
        elif operation == "call":
            action_desc = f"Someone just called your '{name}' method with args {args} and kwargs {kwargs} (METHOD CALL - use wet mode if enabled)"
        else:
            action_desc = f"Someone is doing a '{operation}' operation on '{name}'"

        wet_examples = ""
        if self._wet:
            wet_val = str(self._wet)
            verbose_val = str(self._verbose)
            wet_examples = f"""

WET MODE EXAMPLES (return gremllm objects instead of plain values):
```python
# Instead of: result = 42
# Do this (NO return statement, just set result variable):
result = Gremllm('number', wet={wet_val}, verbose={verbose_val})
result.value = 42
```

```python
# Instead of: result = "hello world"
# Do this (NO return statement, just set result variable):
result = Gremllm('text', wet={wet_val}, verbose={verbose_val})
result.content = "hello world"
```

```python
# Instead of: result = [1, 2, 3]
# Do this (NO return statement, just set result variable):
result = Gremllm('list', wet={wet_val}, verbose={verbose_val})
result.items = [1, 2, 3]
```

IMPORTANT:
- Never use 'return' statements - just set the 'result' variable!
- Always pass wet={wet_val}, verbose={verbose_val} to inherit settings!"""

        return f"""{action_desc}.

Your current memory (self._context): {current_context}

What Python code should be executed? Remember:
- You're a {self._identity}, so implement appropriate behavior
- Store persistent data in _context
- Use 'result' variable for what you want to return
- Just execute the operation directly
- You can import Python libraries, but ONLY use very common ones: json, datetime, math, random, re, os, sys
- DO NOT import: requests, numpy, pandas, beautifulsoup4, PIL, opencv, tensorflow, etc.
- For specialized tasks, implement simple versions yourself rather than importing uncommon libraries
- If you try to import something uncommon, the user will get an error message

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
```{wet_examples}"""

    def _parse_response(self, response_text: str) -> str:
        """Parse the LLM response to extract the code."""
        try:
            # With schema enforcement, this should always be valid JSON
            data = json.loads(response_text)
            code = data.get("code", "")
            # Clean up any stray braces that might have been added
            code = code.strip()
            if code.endswith("}") and code.count("{") < code.count("}"):
                code = code.rstrip("}").strip()
            return code
        except json.JSONDecodeError:
            # Fallback for models that don't support schema (shouldn't happen often)
            text = response_text.strip()
            if text.startswith("```json"):
                text = text[7:]
                if text.endswith("```"):
                    text = text[:-3]
                text = text.strip()
                try:
                    data = json.loads(text)
                    code = data.get("code", "")
                    # Clean up any stray braces
                    code = code.strip()
                    if code.endswith("}") and code.count("{") < code.count("}"):
                        code = code.rstrip("}").strip()
                    return code
                except json.JSONDecodeError:
                    pass
            # Last resort - return the raw text, but clean up stray braces
            text = text.strip()
            if text.endswith("}") and text.count("{") < text.count("}"):
                text = text.rstrip("}").strip()
            return text

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

        # Try to import gremllm for wet mode - only if import succeeds
        try:
            from gremllm import Gremllm

            namespace["Gremllm"] = Gremllm
        except ImportError:
            # If gremllm can't be imported, wet mode won't work but we continue
            pass

        # Execute the code - AI has full access to instance state
        try:
            exec(code, globals(), namespace)
        except ImportError as e:
            # If the generated code tries to import a missing library, return a helpful error
            missing_module = str(e).split("'")[1] if "'" in str(e) else "unknown module"
            namespace["result"] = f"<Gremlin says: Cannot import '{missing_module}' - library not installed>"
        except Exception as e:
            # Handle other execution errors gracefully
            namespace["result"] = f"<Gremlin says: Error executing code: {str(e)}>"

        # Return the result
        return namespace.get("result", None)

    def __repr__(self) -> str:
        """Generate dynamic representation through LLM."""
        try:
            # Only try LLM repr if the object is fully initialized
            if hasattr(self, "_model") and hasattr(self, "_context"):
                return str(self._handle_dynamic_access("get", "__repr__"))
            else:
                return f"<Gremllm({self._identity}) initializing...>"
        except Exception:
            # Fallback to basic representation if LLM fails
            return f"<Gremllm({self._identity}) context={list(self._context.keys())}>"
