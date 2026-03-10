from __future__ import annotations
import heresy


def test_singletonproperty() -> None:
    @heresy.singleton
    class Sample(object):
        _value: int
        def __init__(self):
            self._value = 0
        @heresy.singletonproperty
        def value(self) -> int: # pyright: ignore[reportRedeclaration]
            return self._value
        @value.setter
        def value(self, v: int) -> None:
            self._value = v
    Sample.value = 5
    assert(Sample.value == 5)
