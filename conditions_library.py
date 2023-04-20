import random
from math_tools import is_prime
from utils import randint_N

from utils import Nums, present, ArgType, N, randinterval
from conditions import make_condition, Condition, ConditionFactory

@make_condition(info='No condition.')
def no_condition(nums: Nums) -> bool:
    return True

@make_condition(info='Have 0 even numbers.')
def no_evens(nums: Nums) -> bool:
    return all(i % 2 for i in present(nums))

@make_condition(info='Have 0 odd numbers.')
def no_odds(nums: Nums) -> bool:
    return not any(i % 2 for i in present(nums))

@make_condition(info='Have no duplicates.')
def no_duplicates(nums: Nums) -> bool:
    return all(amount <= 1 for amount in nums.values())

@make_condition(info='Have no primes')
def no_primes(nums: Nums) -> bool:
    return not any(is_prime(num) for num in present(nums))


class number_absent(ConditionFactory):
    requires = ArgType.ONE_INT
    info = 'Don\'t have the number {}'
    def __call__(self, nums: Nums):
        return nums[self.args[0]] == 0

class no_number_from_interval(ConditionFactory):
    requires = ArgType.TWO_INTS
    info = 'Don\'t have any number from the interval [{}, {}]'
    def __call__(self, nums: Nums):
        return not any(self.args[0] <= num <= self.args[1] for num in present(nums))


CONDITIONS = [
    no_condition,
    no_evens, 
    no_odds, 
    no_duplicates,
    no_primes
]

CONDITION_FACTORIES = [
    number_absent,
    no_number_from_interval
]

def get_random_condition() -> Condition:
    # TODO: make this more fair (choose from predefined condition objects too)
    if random.random() < 0.5:
        return random.choice(CONDITIONS)
    
    cf = random.choice(CONDITION_FACTORIES)
    if cf.requires == ArgType.ONE_INT:
        return cf([randint_N(), ])
    elif cf.requires == ArgType.TWO_INTS:
        return cf(randinterval())

# for _ in range(8):
#     cond = get_random_condition()
#     print(cond, cond.get_info())
