from abc import ABC, abstractmethod

from utils import ArgType


class PaymentItem(ABC):
    '''
    Callable[[int], bool]
    '''
    requires: ArgType | None = None
    def __init__(self, args: list[int]) -> None:
        super().__init__()
        self.args = args

    def __repr__(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def __call__(self, num: int) -> bool:
        ...
    
    @abstractmethod
    def difficulty(self) -> float:
        '''
        An indication of how difficult it is to satisfy this payment item
        '''
        ...


Payment = list[PaymentItem]

