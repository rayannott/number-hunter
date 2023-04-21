import random

from math_tools import is_perfect_square, is_power_of_two, is_prime, is_perfect_power
from payments import PaymentItem
from utils import ArgType, randint_N, list_of_randint_N, randinterval


class Literal(PaymentItem):
    requires = ArgType.N_INTS
    def __call__(self, num: int):
        return num in self.args
    def __repr__(self):
        return '|'.join(map(str, self.args))


class Interval(PaymentItem):
    requires = ArgType.TWO_INTS
    def __call__(self, num: int) -> bool:
        # assert len(self.args) == 2
        return self.args[0] <= num <= self.args[1]
    def __repr__(self) -> str:
        return str(tuple(self.args))


class Prime(PaymentItem):
    requires = ArgType.NONE
    def __call__(self, num: int) -> bool:
        return is_prime(num)


class Even(PaymentItem):
    requires = ArgType.NONE
    def __call__(self, num: int) -> bool:
        return num % 2 == 0


class Odd(PaymentItem):
    requires = ArgType.NONE
    def __call__(self, num: int) -> bool:
        return num % 2 == 1


class Square(PaymentItem):
    requires = ArgType.NONE
    def __call__(self, num: int) -> bool:
        return is_perfect_square(num)


class PerfectPower(PaymentItem):
    requires = ArgType.NONE
    def __call__(self, num: int) -> bool:
        return is_perfect_power(num)


class PowerOfTwo(PaymentItem):
    requires = ArgType.NONE
    def __call__(self, num: int) -> bool:
        return is_power_of_two(num)


class Any(PaymentItem):
    requires = ArgType.NONE
    def __call__(self, num: int) -> bool:
        return True
    

class NotPrime(PaymentItem):
    requires = ArgType.NONE
    def __call__(self, num: int) -> bool:
        return not is_prime(num)


PAYMENT_ITEMS: list = [
    Literal,
    Interval,
    Prime,
    NotPrime,
    Even,
    Odd,
    Square,
    PerfectPower,
    PowerOfTwo,
    Any
]
PAYMENT_ITEMS_WEIGHTS: list[int] = [5, 50, 4, 30, 40, 40, 20, 10, 10, 70]

assert len(PAYMENT_ITEMS) == len(PAYMENT_ITEMS_WEIGHTS)

def get_random_payment_item():
    PI = random.choices(PAYMENT_ITEMS, weights=PAYMENT_ITEMS_WEIGHTS, k=1)[0]
    if PI.requires == ArgType.NONE:
        return PI([])
    elif PI.requires == ArgType.ONE_INT:
        return PI([randint_N(), ])
    elif PI.requires == ArgType.TWO_INTS:
        return PI(randinterval())
    elif PI.requires == ArgType.N_INTS:
        return PI(list_of_randint_N(random.randint(1, 3)))

PREDEFINED_PAYMENTS = [
    [Literal([2])],
    [Literal([1])],
    [Even([]), Odd([])],
    [Any([]), Any([])],
    [Prime([])],
    [Square([])],
    [Interval([0, 10])],
    [Interval([89, 99])],
    [Any([])],
]

PREDEFINED_PAYMENTS_WEIGHTS = [2, 1, 10, 15, 3, 5, 10, 10, 30]

def get_random_payment():
    if random.random() < 0.5: # TODO: temporary
        return [get_random_payment_item() for _ in range(random.choices([1,2,3], weights=[8,2,1])[0])]
    return random.choices(PREDEFINED_PAYMENTS, weights=PREDEFINED_PAYMENTS_WEIGHTS)[0]
