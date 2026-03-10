from __future__ import annotations
from typing import TypeVar, Any, Generic
import collections.abc as cabc
import threading
from ._internal.singleton_registry import SingletonRegistry


_T = TypeVar("_T")
_R = TypeVar("_R")


class singletonproperty(Generic[_T, _R]):
    _fget: cabc.Callable[[_T], _R] | None
    _fset: cabc.Callable[[_T, Any], None] | None
    _fdel: cabc.Callable[[_T], None] | None
    _owner: type[_T]
    _lock: threading.Lock

    def __set_name__(self, owner: type[_T], _: str) -> None:
        self._owner = owner

    def __init__(
        self,
        fget: cabc.Callable[[_T], _R] | None = None,
        fset: cabc.Callable[[_T, Any], None] | None = None,
        fdel: cabc.Callable[[_T], None] | None = None,
        doc: str | None = None
    ) -> None:
        self._fget = fget
        self._fset = fset
        self._fdel = fdel
        self._lock = threading.Lock()
        self.__doc__ = doc if doc is not None else (fget.__doc__ if fget else None)

    @property
    def _instance(self) -> _T:
        if self._owner not in SingletonRegistry.data.keys():
            raise TypeError("singletonproperty must only be used inside a singleton.")
        return self._owner()

    def __get__(self, obj: _T | None, _: type[_T] | None = None) -> _R:
        if self._fget is None:
            raise AttributeError("cannot get attribute.")
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

    def getter(self, fget: cabc.Callable[[_T], _R]) -> singletonproperty[_T, _R]:
        self._fget = fget
        return self

    def setter(self, fset: cabc.Callable[[_T, Any], None]) -> singletonproperty[_T, _R]:
        self._fset = fset
        return self

    def deleter(self, fdel: cabc.Callable[[_T], None]) -> singletonproperty[_T, _R]:
        self._fdel = fdel
        return self
