from spyfi import Call
from spyfi import spiffy


class Greeter:
    def holler(self, message: str) -> None:
        print(message.upper())

    def speak(self, message: str) -> None:
        print(message)


class GreeterFactory:
    def make_greeter(self) -> Greeter:
        return Greeter()


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


def test_when_a_spiffy_object_returns_an_object() -> None:
    calls: list[Call] = []
    factory = spiffy(GreeterFactory(), calls.append)

    greeter = factory.make_greeter()
    greeter.holler("ahoy-hoy")

    assert len(calls) == 2
    assert calls[0].method == "make_greeter"
    assert calls[1].method == "holler"
    assert calls[1].args == ("ahoy-hoy",)


def test_when_spyifying_an_object_twice() -> None:
    calls: list[Call] = []
    greeter = spiffy(spiffy(Greeter(), calls.append), calls.append)

    greeter.holler("ahoy-hoy")
    assert len(calls) == 1
