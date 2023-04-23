from abc import ABC, abstractmethod

# from game import Game
from math_tools import PRIMES_UP_TO_N

class Achievement(ABC):
    def __init__(self, name: str, descr: str) -> None:
        self.name = name
        self.descr = descr

    def __repr__(self):
        return self.__class__.__name__
    
    def __eq__(self, other: 'Achievement'):
        return self.name == other.name and self.descr == other.descr
    
    @abstractmethod
    def __hash__(self) -> int:
        ...

    @abstractmethod
    def __call__(self, g) -> bool:
        ...


class AllBelow10(Achievement):
    def __call__(self, g) -> bool:
        return all(g.numbers[i] for i in range(10))
    def __hash__(self) -> int:
        return 1


class AllSquares(Achievement):
    def __call__(self, g) -> bool:
        return all(g.numbers[i**2] for i in range(10))
    def __hash__(self) -> int:
        return 2


class AllPrimes(Achievement):
    def __call__(self, g) -> bool:
        return all(g.numbers[p] for p in PRIMES_UP_TO_N)
    def __hash__(self) -> int:
        return 3


class AllBelow50(Achievement):
    def __call__(self, g) -> bool:
        return all(g.numbers[i] for i in range(50))
    def __hash__(self) -> int:
        return 4

class AllPowersOfTwo(Achievement):
    def __call__(self, g) -> bool:
        return all(g.numbers[2**i] for i in range(7))
    def __hash__(self) -> int:
        return 5


class ALotOfOneNumber(Achievement):
    def __call__(self, g) -> bool:
        return any(v >= 10 for v in g.numbers.values())
    def __hash__(self) -> int:
        return 6


class GetNumberOne(Achievement):
    def __call__(self, g) -> bool:
        return g.numbers[1] > 0
    def __hash__(self) -> int:
        return 7


class TradedFirst10(Achievement):
    def __call__(self, g) -> bool:
        return not any(trade.amount for trade in g.my_trades[:10])
    def __hash__(self) -> int:
        return 8


class TwentyZeros(Achievement):
    def __call__(self, g) -> bool:
        return g.numbers[0] >= 20
    def __hash__(self) -> int:
        return 9
    

class DifferentTrades100(Achievement):
    def __call__(self, g) -> bool:
        return len(g.my_trades) >= 100
    def __hash__(self) -> int:
        return 10


class AllNumbersMoreThanOne(Achievement):
    def __call__(self, g) -> bool:
        return all(v >= 2 for v in g.numbers.values())
    def __hash__(self) -> int:
        return 11


class GoldenMiddle(Achievement):
    def __call__(self, g) -> bool:
        return not (any(g.numbers[i] for i in range(20)) or any(g.numbers[i] for i in range(80, 100)))
    def __hash__(self) -> int:
        return 12


class AllAchievementsBeforeVictory(Achievement):
    def __call__(self, g) -> bool:
        return not g.is_victory() and len(g.achievements) + 1 == len(ACHIEVEMENTS)
    def __hash__(self) -> int:
        return 13


class HugeWallet(Achievement):
    def __call__(self, g) -> bool:
        return g.sum_of_all_numbers() > 12_345
    def __hash__(self) -> int:
        return 14
    

class SumExactly10000(Achievement):
    def __call__(self, g) -> bool:
        return g.sum_of_all_numbers() == 10_000
    def __hash__(self) -> int:
        return 14


ACHIEVEMENTS: list[Achievement] = [
    AllBelow10('Digital Collection', 'Collect all numbers below 10'),
    AllBelow50('Lower Half', 'Collect all numbers below 50'),
    AllPrimes('Prime Minister', 'Collect all prime numbers'),
    AllSquares('Square Fan', 'Collect all perfect square numbers'),
    AllPowersOfTwo('True Programmer', 'Collect all powers of two'),
    ALotOfOneNumber('Dedication', 'Collect 10 or more of any number'),
    GetNumberOne('Unity', 'Get a number 1'),
    TradedFirst10('Trading Amateur', 'Trade all trades with indices below 10'),
    TwentyZeros('A Bunch of Nothing', 'Collect 20 or more zeros'),
    DifferentTrades100('Trading Expert', 'Reach trade index 99'),
    AllNumbersMoreThanOne('Second Round', 'Have at least two of each number'),
    GoldenMiddle('Golden Middle', 'Have zero numbers below 20 and above 80'),
    SumExactly10000('Very Precise', 'Let the sum of your numbers equal 10000'),
    HugeWallet('A Huge Wallet', 'Let the sum of your numbers (including duplicates) exceed 12345'),
    AllAchievementsBeforeVictory('Tough Guy!', 'Complete all achievements before winning')
]


def check_achievements(g) -> set[Achievement]:
    to_ret = set()
    for ach in ACHIEVEMENTS:
        if ach(g):
            to_ret.add(ach)
    return to_ret
