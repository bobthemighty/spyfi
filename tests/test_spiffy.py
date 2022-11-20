from spyfi import Spy


class Greeter:
    def holler(self, message: str) -> None:
        print(message.upper())

    def speak(self, message: str) -> None:
        print(message)


class GreeterFactory:
    def make_greeter(self) -> Greeter:
        return Greeter()


def test_when_an_object_is_spiffy() -> None:
    spy = Spy(Greeter())
    greeter = spy.target

    greeter.speak("hello")
    greeter.holler("hello")

    assert len(spy.calls) == 2
    assert spy.has("speak")
    assert spy.has("speak", "hello")

    assert spy.has("holler", "hello")


def test_when_a_spiffy_object_returns_an_object() -> None:
    spy = Spy(GreeterFactory())
    factory = spy.target

    greeter = factory.make_greeter()
    greeter.holler("ahoy-hoy")

    assert len(spy.calls) == 2
    assert spy.has("make_greeter")
    assert spy.has("holler", "ahoy-hoy")
    assert spy.has("holler")


def test_when_no_call_to_the_method_was_captured() -> None:
    spy = Spy(Greeter())
    greeter = spy.target

    greeter.holler("ahoy-hoy")

    assert spy.has("speak") is False


def test_when_no_call_to_the_method_matches_expected_args() -> None:
    """
    In this test, the captured method expects a single arg, which we
    specify, but the call has the wrong value, so `has` should return
    False.
    """
    spy = Spy(Greeter())
    greeter = spy.target

    greeter.holler("ahoy-hoy")

    assert spy.has("holler", "hoo-boy") is False


def test_when_a_method_is_called_several_times() -> None:
    """
    In this test, the captured method is invoked several times, only
    one of which matches the provided arg.
    """
    spy = Spy(Greeter())
    greeter = spy.target

    greeter.speak("what-ho")
    greeter.speak("hi-hi")
    greeter.speak("oi-oi")

    assert spy.has("speak", "oi-oi") is True
