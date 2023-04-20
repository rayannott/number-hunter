from conditions import Condition
from utils import Nums
from payments import PaymentItem, Payment


class Operation:
    '''
    In-game operation: numbers + condition -> numbers.
    Main way to collect new numbers
    '''
    def __init__(self, cost: Payment, condition: Condition, returns: list[int]) -> None:
        '''
        Give numbers from 'cost' and get numbers from 'returns' if the 'condition' is true
        '''
        self.cost = cost
        self.condition = condition
        self.returns = returns
