from dataclasses import dataclass
import random
from conditions import Condition
from payments_library import Literal
from utils import Nums, ReturnType, list_of_randint_N
from payments import PaymentItem, Payment
from exceptions import ConditionFailedException, WrongNumberOfArguments, InvalidPayment




class Trade:
    '''
    In-game trade: payment + condition -> numbers.
    Main way to collect new numbers
    '''
    def __init__(self, payment: Payment, condition: Condition, returns: ReturnType) -> None:
        '''
        Give numbers from 'payment' and get numbers from 'returns' if the 'condition' is true
        '''
        self.payment = payment
        self.condition = condition
        self.returns = returns

    def check_condition(self, nums: Nums):
        if not self.condition(nums):
            raise ConditionFailedException(f'The condition \'{self.condition}\' is not satisfied.')
    
    def check_args_len(self, args: list[int]):
        if not len(args) == len(self.payment):
            raise WrongNumberOfArguments(f'Wrong number of arguments: entered {len(args)}, required {len(self.payment)}')
    
    def payment_flags(self, args: list[int]) -> list[bool]:
        return [payment_item(arg) for arg, payment_item in zip(args, self.payment)]
    
    def interpret_invalid_payment(self, playment_flags: list[bool]) -> list[str]:
        res = []
        for payment_flag, payment_item in zip(playment_flags, self.payment):
            if not payment_flag:
                res.append(f'{payment_item} is not satisfied')
        return res
        
    def decide_returns(self) -> list[int]:
        match self.returns:
            case ReturnType.RANDOM_NUMS:
                return list_of_randint_N(random.randint(1, 4))
            case ReturnType.PRIME_NUM:
                # TODO
                return []
            case ReturnType.DUPLICATE_LITERALS:
                to_return = []
                for payment_item in self.payment:
                    if isinstance(Literal, payment_item):
                        to_return.extend(payment_item.args)
                return to_return


    def execute(self, args: list[int], nums: Nums) -> list[int]:
        self.check_condition(nums)
        self.check_args_len(args)
        payment_flags = self.payment_flags(args)
        if not all(payment_flags):
            raise InvalidPayment(f'Invalid payment: {", ".join(self.interpret_invalid_payment(payment_flags))}')
        return self.decide_returns()



@dataclass
class TradeM:
    trade: Trade
    amount: int
