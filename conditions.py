from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Callable
from functools import wraps

from utils import Nums, present, ArgType

class Condition(ABC):
    def __init__(self, info: str) -> None:
        super().__init__()
        self.info = info

    def get_info(self):
        return self.info
    
    @abstractmethod
    def __call__(self, nums: Nums) -> bool:
        ...

def make_condition(info: str):
    def decorate(func: Callable):
        class _Condition(Condition):
            def __call__(self, nums: Nums) -> bool:
                return func(nums)
            def __repr__(self) -> str:
                return 'c::' + func.__name__
        this_condition = _Condition(info=info)
        return this_condition
    return decorate

class ConditionFactory(ABC):
    requires: ArgType | None = None
    info: str | None = None

    def __init__(self, args: tuple) -> None:
        self.args = args

    def get_info(self):
        return self.info.format(*self.args)
    
    def __repr__(self):
        return 'cf::' + self.__class__.__name__
    
    @abstractmethod
    def __call__(self, args: tuple) -> Condition:
        ...
