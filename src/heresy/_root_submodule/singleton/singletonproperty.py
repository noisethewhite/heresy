from __future__ import annotations
from typing import TypeVar, ParamSpec, Any, Generic, cast
import collections.abc as cabc
import threading
from ._internal.singleton_registry import SingletonRegistry


_T = TypeVar("_T")
_R = TypeVar("_R")
_P = ParamSpec("_P")


class singletonproperty(Generic[_T, _R]):
    _fget: cabc.Callable[[_T], _R]
    _fset: cabc.Callable[[_T, Any], None] | None
    _fdel: cabc.Callable[[_T], None] | None
    _owner: type[_T] | None
    _lock: threading.Lock

    def __init__(self, fget: cabc.Callable[[_T], _R]) -> None:
        self._fget = fget
        self._fset = None
        self._fdel = None
        self._owner = None
        self._lock = threading.Lock()
        self.__doc__ = fget.__doc__

    def __set_name__(self, owner: type[_T], _: str) -> None:
        self._owner = owner

    @property
    def _instance(self) -> _T:
        if self._owner not in SingletonRegistry.data.keys():
            raise TypeError("singletonproperty must only be used inside a singleton.")
        return cast(type[_T], self._owner)()

    def __get__(self, obj: _T | None, _: type[_T] | None = None) -> _R:
        with self._lock:
            return self._fget(self._instance)

    def __set__(self, _: object, value: Any) -> None:
        if self._fset is None:
            raise AttributeError("cannot set attribute.")
        with self._lock:
            return self._fset(self._instance, value)

    def __delete__(self, _: object) -> None:
        if self._fdel is None:
            raise AttributeError("cannot delete attribute.")
        with self._lock:
            self._fdel(self._instance)

    def setter(self, fset: cabc.Callable[[_T, Any], None]) -> singletonproperty[_T, _R]:
        self._fset = fset
        return self

    def deleter(self, fdel: cabc.Callable[[_T], None]) -> singletonproperty[_T, _R]:
        self._fdel = fdel
        return self
