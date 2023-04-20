import random
from math_tools import is_prime

from utils import Nums, present, ArgType, N
from conditions import make_condition, make_condition_factory, Condition


@make_condition(info='You have 0 even numbers.')
def no_evens(nums: Nums) -> bool:
    return all(i % 2 for i in present(nums))

@make_condition(info='You have 0 odd numbers.')
def no_odds(nums: Nums) -> bool:
    return not any(i % 2 for i in present(nums))

@make_condition(info='You have no duplicates.')
def no_duplicates(nums: Nums) -> bool:
    return all(amount <= 1 for amount in nums.values())

def no_primes(nums: Nums) -> bool:
    return not any(is_prime(num) for num in present(nums))

@make_condition_factory(info='You don\'t have the number {}', requires=ArgType.ONE_INT)
def number_absent(nums: Nums, args: tuple) -> bool:
    number = args[0]
    return nums[number] == 0

@make_condition_factory(info='You don\'t have any number from the interval [{}, {}]', requires=ArgType.TWO_INTS)
def no_number_from_interval(nums: Nums, args: tuple) -> bool:
    return not any(args[0] <= num <= args[1] for num in present(nums))


CONDITIONS = [
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
    if random.random() < 0.5:
        return random.choice(CONDITIONS)
    
    cf = random.choice(CONDITION_FACTORIES)
    if cf.requires == ArgType.ONE_INT:
        return cf((random.randint(1, N), ))
    elif cf.requires == ArgType.TWO_INTS:
        n1, n2 = (random.randint(1, N), (random.randint(1, N)))
        args = (min(n1, n2), max(n1, n2))
        return cf(args)

# for _ in range(8):
#     cond = get_random_condition()
#     print(cond, cond.info)
