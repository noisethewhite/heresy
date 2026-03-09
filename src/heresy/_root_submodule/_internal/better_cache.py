from __future__ import annotations
import collections.abc as cabc
from typing import TypeVar, ParamSpec
import functools


_P = ParamSpec("_P")
_R = TypeVar("_R")


def better_cache(func: cabc.Callable[_P, _R]) -> cabc.Callable[_P, _R]:
    new_func = functools.cache(func)
    @functools.wraps(func)
    def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _R:
        nonlocal new_func
        return new_func(*args, **kwargs)
    return wrapper
