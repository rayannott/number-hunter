from enum import Enum
import random


N = 100
Nums = dict[int, int]


def present(nums: Nums) -> set[int]:
    '''
    Returns a set of present numbers (amount > 0)
    '''
    return {k for k, v in nums.items() if v > 0}


def randint_N() -> int:
    return random.randint(1, N)


def list_of_randint_N(len_: int) -> list[int]:
    return list({randint_N() for _ in range(len_)})


def randinterval() -> int:
    return sorted(list_of_randint_N(2))


class ArgType(Enum):
    ONE_INT = 'one-integer-number'
    TWO_INTS = 'two-integer-numbers'
    NONE = 'no-arguments'
    N_INTS = 'any-amount-of-ints'


class ReturnType(Enum):
    RANDOM_NUMS = 'list-of-random-numbers'
    PRIME_NUM = 'one-random-prime-number'
    DUPLICATE_LITERALS = 'duplicate-all-literals' # Lit(3, 5) -> [3, 3, 5, 5]
    
