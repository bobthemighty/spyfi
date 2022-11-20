# Spyfi

[![PyPI](https://img.shields.io/pypi/v/spyfi.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/spyfi.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/spyfi)][python version]
[![License](https://img.shields.io/pypi/l/spyfi)][license]

[![Read the documentation at https://spyfi.readthedocs.io/](https://img.shields.io/readthedocs/spyfi/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/bobthemighty/spyfi/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/bobthemighty/spyfi/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/spyfi/
[status]: https://pypi.org/project/spyfi/
[python version]: https://pypi.org/project/spyfi
[read the docs]: https://spyfi.readthedocs.io/
[tests]: https://github.com/bobthemighty/spyfi/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/bobthemighty/spyfi
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

A quick and dirty way to turn your existing classes into spies.

## Why though?

I very often create spies for my tests by wrapping an interface around a list, eg.

```python
class FakeEmailSender(list):

    def send(self, address: str, message: str) -> None:
        self.append((address, message))


def test_when_a_customer_signs_up():

    sender = FakeEmailSender()
    handler = SignupHandler(sender)

    handler("user@domain.com", "password")

    assert (("user@domain.com", "welcome to the website")) in sender
```

Sometimes this is a little fiddly, particularly if you need to spy on a hierarchy of objects. Spyfi, pronounced "spiffy", is a quick way to instrument a python object graph and capture calls made to it.

## Installation

You can install _Spyfi_ via [pip] from [PyPI]:

```console
$ pip install spyfi
```

## Usage

```python
from spyfi import Spy


class Thing:

    def __init__(self, colour):
        self.colour = colour

    def say_hello(self, message):
        print(f"Hello, I am a {self.colour} thing: {message})


class ThingFactory:

    def make_thing(self, colour:str) -> Thing:
        return Thing(colour)


def test_thing_messages():

    # Spiffy takes any old object and wraps its methods
    # so that an arbitrary callback receives args and kwargs.
    # In this case, we're appending all calls to a list.
    spy = Spy(ThingFactory())

    # The returned object is otherwise unchanged. `factory` is a real
    # ThingFactory and behaves as normal.
    factory = spy.target
    factory.make_thing("blue").say_hello("I like python")

    # Since we have access to the calls list, we can assert that
    # particular methods were called with the right data.
    assert len(spy.calls) == 2
    assert calls[0].method == "make_thing"
    assert calls[0].args == ("blue",)

    # Spyfi includes a helper method to make assertions easier
    assert spy.has("say_hello")
    assert spy.has("say_hello", "I like python")
```

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_Spyfi_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/bobthemighty/spyfi/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/bobthemighty/spyfi/blob/main/LICENSE
[contributor guide]: https://github.com/bobthemighty/spyfi/blob/main/CONTRIBUTING.md
[command-line reference]: https://spyfi.readthedocs.io/en/latest/usage.html
