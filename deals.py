from utils import Nums
from conditions import Condition
from trades import Trade
from payments import PaymentItem, Payment


class Deal:
    '''
    payment -> 'amount' * 'trade' (TradeM)
    '''
    def __init__(self, payment: Payment, trade: Trade, amount: int) -> None:
        pass
