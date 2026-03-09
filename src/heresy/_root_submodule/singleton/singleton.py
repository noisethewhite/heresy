from __future__ import annotations
from typing import TypeVar, Any, cast
import inspect
from ._internal.singleton_vars import SingletonVars
from ._internal.singleton_registry import SingletonRegistry


_T = TypeVar("_T")


def singleton(_cls: type[_T]) -> type[_T]:
    if len(inspect.signature(_cls.__init__).parameters) != 1:
        raise TypeError(f"{_cls.__name__}.__init__ must only accept 1 argument: self.")

    if _cls not in SingletonRegistry.data:
        SingletonRegistry.data[_cls] = SingletonVars(_cls)
    else:
        raise TypeError("This class is already a singleton.")

    orig_new = _cls.__new__
    orig_init = _cls.__init__

    def __new__(cls: type[_T], *args: Any, **kwargs: Any) -> _T:
        reg_data = SingletonRegistry.data[cls]
        if reg_data.instance is None:
            with reg_data.lock:
                if reg_data.instance is None:
                    reg_data.instance = orig_new(cls, *args, **kwargs)
        return cast(_T, reg_data.instance)

    def __init__(self: object) -> None:
        reg_data = SingletonRegistry.data[type(self)]
        if not reg_data.is_initialized:
            orig_init(cast(_T, self))
            reg_data.is_initialized = True


    setattr(_cls, "__new__", staticmethod(__new__))
    setattr(_cls, "__init__", __init__)

    return _cls
