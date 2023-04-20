import random

from math_tools import is_perfect_square, is_power_of_two, is_prime, is_perfect_power
from payments import PaymentItem
from utils import ArgType, randint_N, list_of_randint_N


class Literal(PaymentItem):
    requires = ArgType.N_INTS
    def __call__(self, num: int):
        return num in self.args
    def __str__(self):
        return '|'.join(map(str, self.args))


class Interval(PaymentItem):
    requires = ArgType.TWO_INTS
    def __call__(self, num: int) -> bool:
        # assert len(self.args) == 2
        return self.args[0] <= num <= self.args[1]
    def __str__(self) -> str:
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


PAYMENT_ITEMS: list = [
    Literal,
    Interval,
    Prime,
    Even,
    Odd,
    Square,
    PerfectPower,
    PowerOfTwo,
    Any
]


def get_random_payment_item():
    PI = random.choice(PAYMENT_ITEMS)
    if PI.requires == ArgType.NONE:
        return PI([])
    elif PI.requires == ArgType.ONE_INT:
        return PI([randint_N(), ])
    elif PI.requires == ArgType.N_INTS:
        return PI(list_of_randint_N())


def get_random_payment():
    return [get_random_payment_item() for _ in range(random.randint(1, 3))]
