from enum import Enum, auto
import random


N = 100
Nums = dict[int, int]
SAVES_DIR = 'saves'


def present(nums: Nums) -> set[int]:
    '''
    Returns a set of present numbers (amount > 0)
    '''
    return {k for k, v in nums.items() if v > 0}


def randint_N() -> int:
    return random.randrange(0, N)


def list_of_randint_N(len_: int) -> list[int]:
    return list({randint_N() for _ in range(len_)})


def randinterval() -> int:
    return sorted(list_of_randint_N(2))


class ArgType(Enum):
    ONE_INT = auto() # 'one-integer-number'
    TWO_INTS = auto() # 'two-integer-numbers'
    NONE = auto() # 'no-arguments'
    N_INTS = auto() # 'any-amount-of-ints'
