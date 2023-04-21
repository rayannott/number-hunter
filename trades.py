from dataclasses import dataclass
import random
from math import prod
from collections import Counter

from payments_library import Literal
from utils import Nums, list_of_randint_N, N
from return_types import ReturnType
from payments import PaymentItem, Payment
from exceptions import ConditionFailedException, WrongNumberOfArguments, InvalidPayment, NotEnoughNumbers
from math_tools import random_prime, closest_prime, digitize, all_prime_factors


class Trade:
    '''
    In-game trade: payment + condition -> numbers.
    Main way to collect new numbers
    '''
    def __init__(self, payment: Payment, returns: ReturnType, multiplier: int) -> None:
        '''
        Give numbers from 'payment' and get numbers from 'returns' times 'multiplier'
        '''
        self.payment = payment
        self.returns = returns
        self.args = None
        self.multiplier = multiplier

    def __repr__(self) -> str:
        return f'{str(self.payment)} -> {self.multiplier}*{self.returns.name}'

    def check_args_len(self, args: list[int]):
        if not len(args) == len(self.payment):
            raise WrongNumberOfArguments(f'Wrong number of arguments: entered {len(args)}, required {len(self.payment)}')
    
    def check_nums_amounts(self, args: list[int], nums: Nums):
        needed_amounts = Counter(args)
        for num, amount_needed in needed_amounts.items():
            if amount_needed > nums[num]:
                raise NotEnoughNumbers(f'You don\'t have enough of {num}')

    def payment_flags(self, args: list[int]) -> list[bool]:
        return [payment_item(arg) for arg, payment_item in zip(args, self.payment)]
    
    def interpret_invalid_payment(self, playment_flags: list[bool]) -> list[str]:
        res = []
        for payment_flag, payment_item in zip(playment_flags, self.payment):
            if not payment_flag:
                res.append(f'{payment_item} is not satisfied')
        return res
    
    def decide_returns(self, args) -> list[int]:
        match self.returns:
            case ReturnType.ADD_ONE:
                to_ret = [(args[0] + 1) % N]
            case ReturnType.DOUBLE:
                to_ret = [(args[0] * 2) % N]
            case ReturnType.DIGITIZE:
                to_ret = digitize(args[0])
            case ReturnType.FACTORIZE:
                to_ret = all_prime_factors(args[0])
            case ReturnType.CLOSEST_PRIME:
                to_ret = [closest_prime(args[0])]
            case ReturnType.RANDOM_NUMS:
                to_ret = list_of_randint_N(
                    random.choices([1, 2, 3, 4, 5], 
                           weights=[1, 5, 15, 8, 5])[0]
                )
            case ReturnType.PRIME_NUM:
                to_ret = [random_prime()]
            case ReturnType.CLONE:
                to_ret =  args * 2
            case ReturnType.SUM:
                to_ret = [sum(args) % N]
            case ReturnType.MULT_NUMS:
                to_ret = [prod(args) % N]
            case ReturnType.MEAN_NUMS:
                to_ret = [round(sum(args)/len(args))]
            case ReturnType.SQUARE:
                to_ret = [el ** 2 % N for el in args]
        return to_ret * self.multiplier

    def execute(self, args: list[int], nums: Nums) -> list[int]:
        self.check_args_len(args)
        self.check_nums_amounts(args, nums)
        payment_flags = self.payment_flags(args)
        if not all(payment_flags):
            raise InvalidPayment(f'Invalid payment: {", ".join(self.interpret_invalid_payment(payment_flags))}')
        return self.decide_returns(args)



@dataclass
class TradeM:
    trade: Trade
    amount: int
    def __repr__(self) -> str:
        return f'{self.amount} x {self.trade}'
