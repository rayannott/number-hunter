from conditions import Condition
from utils import Nums
from payments import PaymentItem, Payment
from exceptions import ConditionFailedException, WrongNumberOfArguments, InvalidPayment

class Trade:
    '''
    In-game trade: numbers + condition -> numbers.
    Main way to collect new numbers
    '''
    def __init__(self, cost: Payment, condition: Condition, returns: list[int]) -> None:
        '''
        Give numbers from 'cost' and get numbers from 'returns' if the 'condition' is true
        '''
        self.cost = cost
        self.condition = condition
        self.returns = returns

    def check_condition(self, nums: Nums):
        if not self.condition(nums):
            raise ConditionFailedException(f'The condition \'{self.condition}\' is not satisfied.')
    
    def check_args_len(self, args: list[int]):
        if not len(args) == len(self.cost):
            raise WrongNumberOfArguments(f'Wrong number of arguments: entered {len(args)}, required {len(self.cost)}')
    
    def payment_flags(self, args: list[int]) -> list[bool]:
        return [payment_item(arg) for arg, payment_item in zip(args, self.cost)]
    
    def interpret_invalid_payment(self, playment_flags: list[bool]) -> list[str]:
        res = []
        for payment_flag, payment_item in zip(playment_flags, self.cost):
            if not payment_flag:
                res.append(f'{payment_item} is not satisfied')
        return res
        
    def execute(self, args: list[int], nums: Nums):
        self.check_condition(nums)
        self.check_args_len(args)
        payment_flags = self.payment_flags(args)
        if not all(payment_flags):
            raise InvalidPayment(f'Invalid payment: {", ".join(self.interpret_invalid_payment(payment_flags))}')
        return self.returns
