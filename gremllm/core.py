import json
import traceback
from typing import Any, Dict, Optional
from .llm import LLMProvider


class Gremllm:
    """
    A dynamic object that uses AI to determine behavior at runtime.
    
    Instead of predefined methods, Gremllm objects ask an LLM what to do
    when methods are called or attributes are accessed.
    """
    
    def __init__(self, identity: str, llm_provider: str = "mock", **kwargs):
        # Use object.__setattr__ to avoid triggering our custom __setattr__
        object.__setattr__(self, '_identity', identity)
        object.__setattr__(self, '_llm', LLMProvider.create(llm_provider, **kwargs))
        object.__setattr__(self, '_context', {})
        
    def __getattr__(self, name: str) -> Any:
        """Handle attribute access dynamically through LLM."""
        if name.startswith('_'):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        
        # For method-like names, return a callable that triggers the LLM with 'call'
        if name in ['increment', 'decrement', 'reset', 'clear', 'add', 'remove', 'update'] or name.endswith('()'):
            def method_caller(*args, **kwargs):
                return self._handle_dynamic_access('call', name, *args, **kwargs)
            return method_caller
            
        # For ALL other attributes (including 'value'), ask LLM what to do
        return self._handle_dynamic_access('get', name)
    
    def __setattr__(self, name: str, value: Any) -> None:
        """Handle attribute assignment dynamically through LLM."""
        if name.startswith('_'):
            object.__setattr__(self, name, value)
            return
            
        # Ask LLM what to do with this assignment
        self._handle_dynamic_access('set', name, value)
    
    def __call__(self, *args, **kwargs):
        """Make the object itself callable."""
        return self._handle_dynamic_access('call', '__call__', *args, **kwargs)
    
    def _handle_dynamic_access(self, operation: str, name: str, *args, **kwargs) -> Any:
        """
        Handle dynamic operations by asking the LLM what to do.
        
        Args:
            operation: 'get', 'set', or 'call'
            name: attribute/method name
            *args, **kwargs: arguments for the operation
        """
        # Prepare context for LLM
        context = {
            'identity': self._identity,
            'operation': operation,
            'name': name,
            'args': args,
            'kwargs': kwargs,
            'current_context': dict(self._context)
        }
        
        try:
            # Get code from LLM
            response = self._llm.generate_code(context)
            
            # Execute the code and return result directly
            result = self._execute_code(response['code'], name, *args, **kwargs)
            return result
            
        except Exception as e:
            # Fallback behavior
            if operation == 'set':
                self._context[name] = args[0] if args else kwargs
                return None
            elif operation == 'get':
                return f"<Gremlin says: Error accessing {name}: {str(e)}>"
            else:
                return f"<Gremlin says: Error in {name}: {str(e)}>"
    
    def _execute_code(self, code: str, method_name: str, *args, **kwargs) -> Any:
        """
        Execute LLM-generated code in the instance context.
        """
        # Create a namespace that gives the AI direct access to instance internals
        # Similar to IPython embed - the AI can access all instance attributes directly
        namespace = self.__dict__.copy()
        namespace.update({
            'args': args,
            'kwargs': kwargs,
            'self': self,
        })
        
        # Execute the code - AI has full access to instance state
        exec(code, globals(), namespace)
        
        # Return the result
        return namespace.get('result', None)
    
    def __repr__(self) -> str:
        return f"<Gremllm({self._identity}) context={list(self._context.keys())}>"
