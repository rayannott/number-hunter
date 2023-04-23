from enum import Enum, auto


class ReturnType(Enum):
    RANDOM_NUMS = auto() # list-of-random-numbers
    RANDOM_PRIME = auto() # one-random-prime-number
    CLONE = auto() # duplicate-all-nums (3, 5) -> [3, 3, 5, 5]
    ADD_ONE = auto() # return num+1
    SUBTRACT_ONE = auto() # return num+1
    DOUBLE = auto() # return num*2 % 100
    DIGITIZE = auto() # return [d for d in digits(num)] * 2
    FACTORIZE = auto() # return [p for p in all_prime_factors(num)] * 2
    SUM = auto() # sum all nums, return sum_ % 100
    CLOSEST_PRIME = auto() # returns prime p closest to num
    MULT_NUMS = auto() # returns a multiple of nums % 100
    MEAN = auto() # returns a mean of nums rounded to closest
    SQUARE = auto()
    CONCATENATE = auto()
    HALVE = auto()
    DIFFERENCE = auto() # returns absolute difference
    UNFOLD = auto()

HELP_RETURN_TYPES: dict[ReturnType, str] = {
    ReturnType.RANDOM_NUMS: 'get from 1 to 5 random numbers',
    ReturnType.RANDOM_PRIME: 'get one random prime number',
    ReturnType.CLONE: 'get the number(s) back twice their amount',
    ReturnType.ADD_ONE: 'get the number(s) incremented by one',
    ReturnType.SUBTRACT_ONE: 'get the number(s) decremented by one',
    ReturnType.DOUBLE: 'get the number(s) doubled',
    ReturnType.DIGITIZE: 'get the number\'s digits',
    ReturnType.FACTORIZE: 'get the number\'s factors',
    ReturnType.SUM: 'get the number\' sum',
    ReturnType.CLOSEST_PRIME: 'get the prime number closest to the given number',
    ReturnType.MULT_NUMS: 'get the product of the numbers',
    ReturnType.MEAN: 'get the mean of the numbers; if not integer, get two numbers: ceil(mean) and floor(mean)',
    ReturnType.SQUARE: 'get the square of the number(s)',
    ReturnType.CONCATENATE: 'get the result of a concatenation of the numbers',
    ReturnType.HALVE: 'get the number divided by two; if not integer, get two numbers: ceil(half) and floor(half)',
    ReturnType.DIFFERENCE: 'get the absolute difference between two numbers',
    ReturnType.UNFOLD: 'get one less and one more of the given number: num-1 and num+1'
}

GROUPS_BY_PAYMENT_LEN: dict[str, tuple[list[ReturnType], list[int]]] = {
    'any': (
    [
        ReturnType.RANDOM_NUMS,
        ReturnType.RANDOM_PRIME,
        ReturnType.CLONE,
        ReturnType.SQUARE,
        ReturnType.ADD_ONE,
        ReturnType.SUBTRACT_ONE,
    ], [15, 6, 20, 7, 15, 15]),
    'one': (
    [
        ReturnType.DOUBLE,
        ReturnType.DIGITIZE,
        ReturnType.FACTORIZE,
        ReturnType.CLOSEST_PRIME,
        ReturnType.HALVE,
        ReturnType.UNFOLD
    ], [13, 12, 12, 7, 13, 15]),
    'not_one': (
    [
        ReturnType.SUM,
        ReturnType.MULT_NUMS,
        ReturnType.CONCATENATE,
    ], [8, 11, 8]),
    'two': (
    [
        ReturnType.MEAN,
        ReturnType.DIFFERENCE
    ], [5, 13])
}

for key, (r_types, weights) in GROUPS_BY_PAYMENT_LEN.items():
    assert len(r_types) == len(weights)
