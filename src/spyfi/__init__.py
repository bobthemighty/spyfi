"""Spyfi."""
import inspect
from dataclasses import dataclass
from functools import wraps
from typing import Any
from typing import Callable
from typing import Tuple
from typing import TypeVar


TAG = "__SPYIFIED"
T = TypeVar("T")
TInput = TypeVar("TInput")
F = Callable[..., Any]


@dataclass
class Call:
    """Captures the name, args, and kwargs of a spied function."""

    method: str
    args: Tuple[Any, ...]
    kwargs: dict[str, Any]


Handler = Callable[[Call], None]


def _decorator(func: Callable[..., T], callback: Handler) -> Callable[..., T]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        callback(Call(func.__name__, args, kwargs))
        return spiffy(func(*args, **kwargs), callback)

    return wrapper


def magic(name: str) -> bool:
    return name.startswith("__")


def tagged(x: Any) -> Any:
    return getattr(x, TAG, False) is True


def tag(x: Any) -> None:
    setattr(x, TAG, True)


def spiffy(x: T, handler: Handler) -> T:
    """Wraps a type for spying.

    Every public method of the type will be decorated to invoke handler
    with a Call object capturing the args, kwargs, and method name.
    """
    if x is None:
        return x  # type: ignore
    if tagged(x):
        return x
    for name, func in inspect.getmembers(x):
        if inspect.ismethod(func) and not magic(name):
            setattr(x, name, _decorator(func, handler))
    tag(x)
    return x


__all__ = ["spiffy", "Call"]
