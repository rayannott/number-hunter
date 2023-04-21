import random
from trades import TradeM
from utils import N
from trades_library import get_random_trade
from exceptions import EmptyTradeM, CustomException
from utils import list_of_randint_N

class Game:
    def __init__(self) -> None:
        '''
        :param N: number of integers to collect (from 0 to N-1)
        '''
        self.numbers = {i: 0 for i in range(N)}
        for el in list_of_randint_N(10):
            self.numbers[el] += 1
        self.my_trades: list[TradeM] = [get_random_trade() for _ in range(10)]
        self.available_deals = []

    def is_victory(self):
        return all(self.numbers.values())

    def trade(self, chosen_trade_index: int, args: list[int]) -> list[int]:
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
            gifted_trade = None if random.random() < 0.5 else get_random_trade()
            if gifted_trade:
                self.my_trades.append(gifted_trade)
            return returns, gifted_trade
            

    def buy(self, chosen_deal_index: int, args: list[int]):
        chosen_deal = self.available_deals[chosen_deal_index]
        # TODO
    
    def roll(self):
        # TODO
        pass