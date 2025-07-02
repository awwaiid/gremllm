from .core import Gremllm


def new(identity, model="gpt-4o-mini", **kwargs):
    """Create a new Gremllm instance with the given identity."""
    return Gremllm(identity=identity, model=model, **kwargs)


__all__ = ["new", "Gremllm"]
