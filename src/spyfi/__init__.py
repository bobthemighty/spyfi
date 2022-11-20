"""Spyfi."""
import inspect
from dataclasses import dataclass
from functools import wraps
from typing import Any
from typing import Callable
from typing import Generic
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


class Spy(Generic[T]):
    """Wraps a target object and instruments public method calls."""

    def __init__(self, target: T) -> None:
        """Creates a new Spy wrapping over target."""
        self.target = target
        self.calls: list(Call) = []
        self._instrument(self.target)

    def _instrument(self, target):
        if target is None or tagged(target):
            return target  # type: ignore
        for name, func in inspect.getmembers(target):
            if inspect.ismethod(func) and not magic(name):
                setattr(target, name, self._decorate(func))
        tag(target)
        return target

    def _decorate(self, func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            self.calls.append(Call(func.__name__, args, kwargs))
            return self._instrument(func(*args, **kwargs))

        return wrapper

    def has(self, name, *args, **kwargs) -> bool:
        """Searches captured calls.

        Args:
            name: The name of the captured method.
            args: The exhaustive set of args passed to the method.
            kwargs: The kwargs passed to the method.
        """
        for call in self.calls:
            if call.method == name:
                return (not args) or (args == call.args)
        return False


Handler = Callable[[Call], None]


def magic(name: str) -> bool:
    return name.startswith("__")


def tagged(x: Any) -> Any:
    return getattr(x, TAG, False) is True


def tag(x: Any) -> None:
    setattr(x, TAG, True)


__all__ = ["Spy", "Call"]
