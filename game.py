import random

from trades import TradeM, Trade
from utils import N_FOR_BARGAIN, N_FOR_MEGA_BARGAIN, TRADES_BOUND, GameInfo, N
from trades_library import get_random_trade
from exceptions import (
    EmptyTradeM,
    CustomException,
    NumbersNotUnique,
    BargainWrongNumberOfArgs,
    InvalidTradeIndex,
    TooManyTradingIndices,
)
from utils import list_of_randint_N
from achievements import check_achievements, Achievement, ACHIEVEMENTS


class Game:
    def __init__(self, gi: GameInfo) -> None:
        self.info = gi
        self.numbers = {i: 0 for i in range(N)}
        for el in list_of_randint_N(self.info.init_nums):
            self.numbers[el] += 1
        self.my_trades: list[TradeM] = [
            get_random_trade() for _ in range(self.info.init_trades)
        ]
        self.victory = False
        self.achievements: set[Achievement] = set()
        self.times_traded = 0
        self.shown_you_won_message = False
        self.achievements.update(check_achievements(self))
        print(self.victory)

    def pre_start(self):
        if self.is_victory():
            print("You won this game!")
            for ach in self.achievements:
                ach.activate()
            for ach in ACHIEVEMENTS:
                ach.activate()

    def is_victory(self):
        return self.victory or all(self.numbers.values())

    def trade(
        self, chosen_trade_index: int, args: list[int]
    ) -> tuple[list[int], TradeM | None]:
        if len(self.achievements) >= 2 and (
            num_trades := self.num_active_trade_indices()
        ) > TRADES_BOUND + len(self.achievements):
            raise TooManyTradingIndices(
                f"Number of active trades must not exceed {TRADES_BOUND + len(self.achievements)}; you currently have {num_trades}"
            )
        try:
            chosen_tradem = self.my_trades[chosen_trade_index]
        except IndexError:
            raise InvalidTradeIndex(f"Index {chosen_trade_index} is out of range")
        chosen_trade = chosen_tradem.trade
        if chosen_tradem.amount == 0:
            raise EmptyTradeM("You have 0 of this trade")
        try:
            returns = chosen_trade.execute(args, self.numbers)
        except CustomException as e:
            raise e
        else:
            # successful trade
            for arg in args:
                self.numbers[arg] -= 1
            for num in returns:
                self.numbers[num] += 1
            self.times_traded += 1
            chosen_tradem.amount -= 1
            gifted_trade = None if random.random() < 0.05 else get_random_trade()
            if gifted_trade:
                self.my_trades.append(gifted_trade)
            return returns, gifted_trade

    def check_achievements(self):
        completed_achievements = check_achievements(self)
        difference = completed_achievements.difference(self.achievements)
        self.achievements.update(completed_achievements)
        return difference

    def num_active_trade_indices(self):
        return len([1 for tr in self.my_trades if tr.amount])

    def sum_of_all_numbers(self):
        return sum(k * v for k, v in self.numbers.items())

    def sell(self, trade_ids: list[int]) -> list[int]:
        for trade_id in trade_ids:
            try:
                _ = self.my_trades[trade_id]
            except IndexError:
                raise InvalidTradeIndex(f"Invalid index for a trade: {trade_id}")

        total_sold = 0
        for trade_id in trade_ids:
            total_sold += self.my_trades[trade_id].amount
            self.my_trades[trade_id].amount = 0

        returns = []
        for _ in range(total_sold):
            returns.extend(list_of_randint_N(random.randint(1, 2)))

        for num in returns:
            self.numbers[num] += 1
        return returns

    def bargain(self, args: list[int]) -> list[TradeM]:
        """
        Give away N_FOR_BARGAIN different numbers and get one random trade.
        """
        if len(args) != len(set(args)):
            raise NumbersNotUnique(f"Numbers are not unique: {args}")
        if len(args) not in [N_FOR_BARGAIN, N_FOR_MEGA_BARGAIN]:
            raise BargainWrongNumberOfArgs(
                f"Needs {N_FOR_BARGAIN} or {N_FOR_MEGA_BARGAIN} unique numbers; got {len(args)}"
            )

        Trade.check_nums_amounts(args, self.numbers)

        for arg in args:
            self.numbers[arg] -= 1

        if len(args) == N_FOR_BARGAIN:
            return [get_random_trade(is_bargain=True)]
        else:
            return [get_random_trade(is_bargain=True) for i in range(4)]
