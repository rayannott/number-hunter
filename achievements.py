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
    

ACHIEVEMENTS: list[Achievement] = [
    AllBelow10('Digital Collection', 'Collect all numbers below 10'),
    AllBelow50('Lower Half', 'Collect all numbers below 50'),
    AllPrimes('Primer in Ntheory', 'Collect all prime numbers'),
    AllSquares('Square Fan', 'Collect all perfect square numbers'),
    AllPowersOfTwo('True Programmer', 'Collect all powers of two'),
    ALotOfOneNumber('Dedication', 'Collect 10 or more of one number'),
    GetNumberOne('Unity', 'Get a number 1'),
    TradedFirst10('Trading Amateur', 'Trade all trades with indices below 10'),
    TwentyZeros('A bunch of 0s', 'Collect 20 or more zeros')
]


def check_achievements(g) -> set[Achievement]:
    to_ret = set()
    for ach in ACHIEVEMENTS:
        if ach(g):
            to_ret.add(ach)
    return to_ret
