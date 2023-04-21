import random

from trades import TradeM
from utils import GameInfo, N
from trades_library import get_random_trade
from exceptions import EmptyTradeM, CustomException
from utils import list_of_randint_N
from achievements import check_achievements, Achievement


class Game:
    def __init__(self, gi: GameInfo) -> None:
        self.info = gi
        self.numbers = {i: 0 for i in range(N)}
        for el in list_of_randint_N(10):
            self.numbers[el] += 1
        self.my_trades: list[TradeM] = [get_random_trade() for _ in range(10)]
        self.available_deals = []
        self.achievements: set[Achievement] = set()

    def is_victory(self):
        return all(self.numbers.values())

    def trade(self, chosen_trade_index: int, args: list[int]) -> tuple[list[int], TradeM, set[Achievement]]:
        chosen_tradem = self.my_trades[chosen_trade_index]
        chosen_trade = chosen_tradem.trade
        if chosen_tradem.amount == 0:
            raise EmptyTradeM('You have 0 of this trade')
        try:
            returns = chosen_trade.execute(args, self.numbers)
        except CustomException as e:
            raise e
        else:
            # successful trade
            for num in returns:
                self.numbers[num] += 1
            for arg in args:
                self.numbers[arg] -= 1

            chosen_tradem.amount -= 1
            if chosen_tradem == 0:
                # remove empty tradems
                pass
            gifted_trade = None if random.random() < 0.05 else get_random_trade()
            if gifted_trade:
                self.my_trades.append(gifted_trade)

            completed_achievements = check_achievements(self.numbers)
            difference = completed_achievements.difference(self.achievements)
            print('new achievements', difference)
            self.achievements.update(completed_achievements)
            return returns, gifted_trade, difference
            
    def roll(self):
        # TODO
        pass
