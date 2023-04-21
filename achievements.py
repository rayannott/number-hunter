from abc import ABC, abstractmethod

from utils import Nums

class Achievement(ABC):
    def __init__(self, name: str, descr: str) -> None:
        self.name = name
        self.descr = descr

    def __repr__(self):
        return self.__class__.__name__
    
    @abstractmethod
    def __call__(self, nums: Nums) -> bool:
        ...


class OneDigitNumbers(Achievement):
    def __call__(self, nums: Nums) -> bool:
        return all(nums[i] for i in range(10))


class AllSquares(Achievement):
    def __call__(self, nums: Nums) -> bool:
        return ...
    

class AllPrimes(Achievement):
    def __call__(self, nums: Nums) -> bool:
        return ...
    

class AllBelow50(Achievement):
    def __call__(self, nums: Nums) -> bool:
        return all(nums[i] for i in range(10))
    


ACHIEVEMENTS = [
    OneDigitNumbers('Digital collection', 'Collect all numbers below 10'),

]

def check_achievements(nums: Nums) -> list[Achievement]:
    to_ret = []
    for ach in ACHIEVEMENTS:
        if ach(nums):
            to_ret.append(ach)
    return to_ret
