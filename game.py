import random

from trades import TradeM, Trade
from utils import N_FOR_BARGAIN, GameInfo, N
from trades_library import get_random_trade
from exceptions import EmptyTradeM, CustomException, NumbersNotUnique, BargainWrongNumberOfArgs, InvalidTradeIndex
from utils import list_of_randint_N
from achievements import check_achievements, Achievement


class Game:
    def __init__(self, gi: GameInfo) -> None:
        self.info = gi
        self.numbers = {i: 0 for i in range(N)}
        for el in list_of_randint_N(10):
            self.numbers[el] += 1
        self.my_trades: list[TradeM] = [get_random_trade() for _ in range(10)]
        self.achievements: set[Achievement] = check_achievements(self.numbers)

    def is_victory(self):
        return all(self.numbers.values())

    def trade(self, chosen_trade_index: int, args: list[int]) -> tuple[list[int], TradeM]:
        try:
            chosen_tradem = self.my_trades[chosen_trade_index]
        except IndexError:
            raise InvalidTradeIndex(f'Index {chosen_trade_index} is out of range')
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
            gifted_trade = None if random.random() < 0.05 else get_random_trade()
            if gifted_trade:
                self.my_trades.append(gifted_trade)
            return returns, gifted_trade
    
    def check_achievements(self):
        completed_achievements = check_achievements(self.numbers)
        difference = completed_achievements.difference(self.achievements)
        self.achievements.update(completed_achievements)
        return difference

    def sell(self, chosen_trade_index: int) -> list[int]:
        chosen_tradem = self.my_trades[chosen_trade_index]
        if chosen_tradem.amount == 0:
            raise EmptyTradeM('You have 0 of this trade')
        chosen_tradem.amount -= 1
        returns = list_of_randint_N(random.randint(1, 2))
        for num in returns:
                self.numbers[num] += 1
        return returns

    def bargain(self, args: list[int]) -> TradeM:
        '''
        Give away N_FOR_BARGAIN different numbers and get one random trade. 
        '''
        if len(args) != len(set(args)):
            raise NumbersNotUnique(f'Numbers are not unique: {args}')
        if len(args) != N_FOR_BARGAIN:
            raise BargainWrongNumberOfArgs(f'Needs {N_FOR_BARGAIN} unique numbers; got {len(args)}')
        Trade.check_nums_amounts(args, self.numbers)
        for arg in args:
                self.numbers[arg] -= 1
        return get_random_trade()
