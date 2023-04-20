from utils import Nums, present, ArgType
from conditions import make_condition, make_condition_factory


@make_condition(info='You have 0 even numbers.')
def no_evens(nums: Nums) -> bool:
    return all(i % 2 for i in present(nums))

@make_condition(info='You have 0 odd numbers.')
def no_odds(nums: Nums) -> bool:
    return not any(i % 2 for i in present(nums))

@make_condition(info='You have no duplicates.')
def no_duplicates(nums: Nums) -> bool:
    return all(amount <= 1 for amount in nums.values())


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
    no_duplicates
]

CONDITION_FACTORIES = [
    number_absent,
    no_number_from_interval
]

# for cond in conditions:
#     print(type(cond), cond, cond.info)

print(number_absent)
print(number_absent.info)
na = number_absent((15, ))
print(na)
print(na.info)
print(na({15: 0}))
print(na({15: 3}))