from trades import TradeM
from utils import N

class Game:
    def __init__(self) -> None:
        '''
        :param N: number of integers to collect (from 1 to N)
        '''
        self.numbers = {i: 0 for i in range(1, N+1)}
        self.my_trades: list[TradeM] = []
        self.available_deals = []

    def is_victory(self):
        return all(self.numbers.values())

    def trade(self, chosen_trade_index: int, args: list[int]):
        chosen_trade_with_amount = self.my_trades[chosen_trade_index]
        chosen_trade = chosen_trade_with_amount.trade
        try:
            returns = chosen_trade.execute(args, self.numbers)
        except Exception as e:
            raise e
        else:
            # successful trade
            for num in returns:
                self.numbers[num] += 1
            

    def buy(self, chosen_deal_index: int, args: list[int]):
        chosen_deal = self.available_deals[chosen_deal_index]
        # TODO
    
    def roll(self):
        # TODO
        pass