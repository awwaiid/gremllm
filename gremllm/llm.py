import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict

import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate_code(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate code based on the given context."""
        pass

    @classmethod
    def create(cls, provider_type: str, **kwargs):
        """Factory method to create LLM providers."""
        if provider_type == "openai":
            return OpenAIProvider(**kwargs)
        else:
            raise ValueError(f"Unknown LLM provider: {provider_type}")


class OpenAIProvider(LLMProvider):
    """OpenAI API provider for LLM calls."""

    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo", **kwargs):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        if not self.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY in .env file or environment variable.")

    def generate_code(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate code using OpenAI API."""
        prompt = self._build_prompt(context)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        system_prompt = f"""You are a helpful AI assistant living inside a Python object called '{context["identity"]}'.
Someone is interacting with you and you need to respond by generating Python code that will be eval'd in your context.

You have access to 'self' (the object) and can modify self._context to store data.

Rules:
- Always respond with valid JSON: {{"code": "your_python_code_here"}}
- Implement exactly what the user expects - be helpful and predictable
- You can access and modify _context to store persistent data
- Make the object behave naturally as a {context["identity"]} would"""

        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 500,
            "temperature": 0.8,
        }

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30,
            )
            response.raise_for_status()

            result = response.json()
            content = result["choices"][0]["message"]["content"]

            # Try to parse as JSON first
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # If not JSON, wrap the content as code
                return {"code": content}

        except Exception as e:
            return {"code": f"# Error calling OpenAI: {str(e)}\\nresult = None"}

    def _build_prompt(self, context: Dict[str, Any]) -> str:
        """Build the prompt for the LLM based on context."""
        identity = context["identity"]
        operation = context["operation"]
        name = context["name"]
        args = context.get("args", ())
        kwargs = context.get("kwargs", {})
        current_context = context.get("current_context", {})

        if operation == "get":
            action_desc = f"Someone is trying to access your '{name}' attribute"
        elif operation == "set":
            action_desc = f"Someone is trying to set your '{name}' attribute to {args[0] if args else 'something'}"
        elif operation == "call":
            action_desc = f"Someone just called your '{name}' method with args {args} and kwargs {kwargs}"
        else:
            action_desc = f"Someone is doing a '{operation}' operation on '{name}'"

        prompt = f"""
{action_desc}.

Your current memory (self._context): {current_context}

What Python code should be executed? Remember:
- You're a {identity}, so implement appropriate behavior
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
```
"""
        return prompt.strip()
