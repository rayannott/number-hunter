from enum import Enum

N = 100
Nums = dict[int, int]

def present(nums: Nums) -> set[int]:
    '''
    Returns a set of present numbers (amount > 0)
    '''
    return {k for k, v in nums.items() if v > 0}

class ArgType(Enum):
    ONE_INT = 'one-integer-number'
    TWO_INTS = 'two-integer-numbers'
