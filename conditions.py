from abc import ABC, abstractclassmethod
from collections.abc import Callable
from typing import Callable
from functools import wraps

from utils import Nums, present, ArgType

class Condition(ABC):
    def __init__(self, info: str) -> None:
        super().__init__()
        self.info = info
    @abstractclassmethod
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
    def __init__(self, info: str, requires: ArgType) -> None:
        '''
        Creates a Condition object using some arguments. Arguments' type is specified in 'requires'
        '''
        super().__init__()
        self.info = info
        self.requires = requires
    @abstractclassmethod
    def __call__(self, args: tuple) -> Condition:
        ...


def make_condition_factory(info: str, requires: ArgType):
    def decorate(func: Callable):
        class _ConditionFactory(ConditionFactory):
            def __call__(self, args: tuple) -> Condition:
                class _Condition(Condition):
                    def __call__(self, nums: Nums) -> bool:
                        return func(nums, args)
                    def __repr__(self) -> str:
                        return 'c::' + func.__name__
                return _Condition(info=info.format(*args))
            def __repr__(self) -> str:
                return 'cf::' + func.__name__
        this_condition_factory = _ConditionFactory(info=info, requires=requires)
        return this_condition_factory
    return decorate


