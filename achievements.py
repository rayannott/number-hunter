from abc import ABC, abstractmethod

from utils import Nums
from math_tools import PRIMES_UP_TO_N

class Achievement(ABC):
    def __init__(self, name: str, descr: str) -> None:
        self.name = name
        self.descr = descr

    def __repr__(self):
        return self.__class__.__name__
    
    def __hash__(self) -> int:
        return hash(self.name + self.descr)

    @abstractmethod
    def __call__(self, nums: Nums) -> bool:
        ...


class AllBelow10(Achievement):
    def __call__(self, nums: Nums) -> bool:
        return all(nums[i] for i in range(10))


class AllSquares(Achievement):
    def __call__(self, nums: Nums) -> bool:
        return all(nums[i**2] for i in range(10))
    

class AllPrimes(Achievement):
    def __call__(self, nums: Nums) -> bool:
        return all(nums[p] for p in PRIMES_UP_TO_N)
    

class AllBelow50(Achievement):
    def __call__(self, nums: Nums) -> bool:
        return all(nums[i] for i in range(50))
    

class AllPowersOfTwo(Achievement):
    def __call__(self, nums: Nums) -> bool:
        return all(nums[2**i] for i in range(7))
    

class ALotOfOneNumber(Achievement):
    def __call__(self, nums: Nums) -> bool:
        return any(v >= 10 for v in nums.values())


class GetNumberOne(Achievement):
    def __call__(self, nums: Nums) -> bool:
        return nums[1] > 0

ACHIEVEMENTS: list[Achievement] = [
    AllBelow10('Digital Collection', 'Collect all numbers below 10'),
    AllBelow50('Lower Half', 'Collect all numbers below 50'),
    AllSquares('Square Fan', 'Collect all perfect square numbers'),
    AllPowersOfTwo('True Programmer', 'Collect all powers of two'),
    ALotOfOneNumber('Dedication', 'Collect 10 or more of one number'),
    GetNumberOne('Unity', 'Get a number 1')
]

def check_achievements(nums: Nums) -> set[Achievement]:
    to_ret = set()
    for ach in ACHIEVEMENTS:
        if ach(nums):
            to_ret.add(ach)
    return to_ret
