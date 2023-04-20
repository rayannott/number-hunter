from abc import ABC, abstractclassmethod
from collections.abc import Callable

from utils import Nums

class Condition(ABC):
    @abstractclassmethod
    def __call__(self, nums: Nums) -> bool:
        ...

def make_condition(func: Callable):
    class _Condition(Condition):
        def __call__(self, nums: Nums) -> bool:
            return func(nums)
    this_condition = _Condition()
    return this_condition

class ConditionFactory(ABC):
    @abstractclassmethod
    def __call__(self, nums: Nums) -> bool:
        ...

def make_condition_factory(func: Callable):
    class _ConditionFactory(ConditionFactory):
        def __call__(self, nums: Nums) -> Condition:
            return func(nums)
    this_condition_f = _ConditionFactory()
    return this_condition_f


@make_condition
def no_evens(nums: Nums):
    return all(i % 2 for i in nums)

@make_condition
def no_odds(nums: Nums):
    return not any(i % 2 for i in nums)

