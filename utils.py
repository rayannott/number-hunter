from dataclasses import dataclass
from enum import Enum, auto
import random
from datetime import datetime
from string import ascii_letters


N = 100
Nums = dict[int, int]
N_FOR_BARGAIN = 4
N_FOR_MEGA_BARGAIN = 7
SAVES_DIR = "saves"
TRADES_BOUND = 20


def present(nums: Nums) -> set[int]:
    """
    Returns a set of present numbers (amount > 0)
    """
    return {k for k, v in nums.items() if v > 0}


def randint_N() -> int:
    return random.randrange(0, N)


def list_of_randint_N(len_: int) -> list[int]:
    return list(randint_N() for _ in range(len_))


def randinterval() -> list[int]:
    n1 = randint_N()
    n2 = randint_N()
    while n2 == n1:
        n2 = randint_N()
    return [min(n1, n2), max(n1, n2)]


class ArgType(Enum):
    ONE_INT = auto()  # 'one-integer-number'
    TWO_INTS = auto()  # 'two-integer-numbers'
    NONE = auto()  # 'no-arguments'
    N_INTS = auto()  # 'any-amount-of-ints'


@dataclass
class GameInfo:
    save_name: str = "".join(random.choices(ascii_letters, k=10)) + ".pi"
    date_created_timestamp: float = datetime.timestamp(datetime.now())
    init_nums: int = 10
    init_trades: int = 10

    def __str__(self) -> str:
        return f"{self.save_name}; created on {datetime.fromtimestamp(self.date_created_timestamp)}; started with {self.init_nums} nums and {self.init_trades} trades"
