from __future__ import annotations
import heresy


def test_singleton() -> None:
    @heresy.singleton
    class Sample(object):
        def __init__(self):
            pass
    a = Sample()
    b = Sample()
    assert(a is b)
