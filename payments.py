from abc import ABC, abstractmethod

from utils import ArgType
class PaymentItem(ABC):
    '''
    Callable[[int], bool]
    '''
    @abstractmethod
    def __call__(self, num: int) -> bool:
        ...
    @abstractmethod
    def __str__(self) -> str:
        ...
Payment = list[PaymentItem]


class Lit(PaymentItem):
    '''
    Any of the 'numbers'
    '''
    requires = ArgType.N_INTS
    def __init__(self, numbers: list[int]) -> None:
        super().__init__()
        self.numbers = numbers
    def __call__(self, num: int):
        return num in self.numbers
    def __str__(self):
        return '|'.join(map(str, self.numbers))

class Interval(PaymentItem):
    '''
    Any number from the interval
    '''
    requires = ArgType.TWO_INTS
    def __init__(self, interval: list[int]) -> None:
        assert len(interval) == 2
        super().__init__()
        self.ivl = interval
    def __call__(self, num: int) -> bool:
        return self.ivl[0] <= num <= self.ivl[1]
    def __str__(self) -> str:
        return str(tuple(self.ivl))
