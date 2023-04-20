from abc import ABC, abstractmethod
from math_tools import is_prime

from utils import ArgType


class PaymentItem(ABC):
    '''
    Callable[[int], bool]
    '''
    requires: ArgType | None = None
    def __init__(self, args: list[int]) -> None:
        super().__init__()
        self.args = args

    def __str__(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def __call__(self, num: int) -> bool:
        ...


Payment = list[PaymentItem]

