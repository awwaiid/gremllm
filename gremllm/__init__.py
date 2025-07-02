from .core import Gremllm


def new(identity, llm_provider="openai", **kwargs):
    """Create a new Gremllm instance with the given identity."""
    return Gremllm(identity=identity, llm_provider=llm_provider, **kwargs)


__all__ = ["new", "Gremllm"]
