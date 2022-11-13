#!/usr/bin/env python3
from dataclasses import dataclass
from functools import wraps
import inspect
from typing import Any
from typing import Callable
from typing import Tuple
from typing import TypeVar


T = TypeVar("T")
TInput = TypeVar("TInput")
TReturn = TypeVar("TReturn")


@dataclass
class Call:
    method: str
    args: Tuple[Any]
    kwargs: dict[str, Any]


Handler = Callable[[Call], None]


def _decorator(
    f: Callable[[TInput], TReturn], callback: Handler
) -> Callable[[TInput], TReturn]:
    @wraps(f)
    def wrapper(*args, **kwargs):
        callback(Call(f.__name__, args, kwargs))
        return f

    return wrapper


def magic(name: str) -> bool:
    return name.startswith("__")


def spiffy(x: T, handler: Handler) -> T:
    for name, func in inspect.getmembers(x):
        if inspect.ismethod(func) and not magic(name):
            setattr(x, name, _decorator(func, handler))
    return x


class Greeter:
    def holler(self, message: str) -> None:
        print(message.upper())

    def speak(self, message: str) -> None:
        print(message)


def test_when_an_object_is_spiffy() -> None:
    calls: list[Call] = []
    greeter = spiffy(Greeter(), calls.append)

    greeter.speak("hello")
    greeter.holler("hello")

    assert len(calls) == 2
    assert calls[0].method == "speak"
    assert calls[0].args == ("hello",)

    assert calls[1].method == "holler"
    assert calls[1].args == ("hello",)
