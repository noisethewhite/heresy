from __future__ import annotations
from ._version import __version__
from ._root_submodule.singleton.singleton import singleton
from ._root_submodule.singleton.singletonproperty import singletonproperty
from ._root_submodule.singleton.singletonmethod import singletonmethod

__all__: list[str] = ["__version__", "singleton", "singletonproperty", "singletonmethod"]
