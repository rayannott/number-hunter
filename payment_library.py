from math_tools import is_perfect_square, is_prime, is_perfect_power
from payments import PaymentItem
from utils import ArgType


class Literal(PaymentItem):
    '''
    Any of the 'numbers'
    '''
    requires = ArgType.N_INTS
    def __call__(self, num: int):
        return num in self.args
    def __str__(self):
        return '|'.join(map(str, self.args))


class Interval(PaymentItem):
    '''
    Any number from the interval
    '''
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


class Any(PaymentItem):
    requires = ArgType.NONE
    def __call__(self, num: int) -> bool:
        return True


PAYMENT_ITEMS = [
    Literal,
    Interval,
    Prime,
    Even,
    Odd,
    Square,
    Any
]