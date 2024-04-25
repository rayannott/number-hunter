import random

from trades import Trade, TradeM
from return_types import GROUPS_BY_PAYMENT_LEN, ReturnType
from payments_library import get_random_payment


PREDEFINED_TRADEMS = [

]

PREDEFINED_TRADEMS_WEIGHTS = [

]

assert len(PREDEFINED_TRADEMS) == len(PREDEFINED_TRADEMS_WEIGHTS)


def get_random_trade(is_bargain: bool = False) -> TradeM:
    # if random.random() < 0.1:
    #     return random.choices(PREDEFINED_TRADEMS, weights=PREDEFINED_TRADEMS_WEIGHTS)[0]
    
    amount = random.choices([1,2,3,4,5], weights=[20, 20, 5, 2, 1], k=1)[0]
    payment = get_random_payment()
    cum_difficulty = 0
    for payment_item in payment:
        cum_difficulty += payment_item.difficulty()
    cum_difficulty += 0.1 * len(payment)
    multiplier = min(5, max(1, round(cum_difficulty * 5)))
    random_number = random.random()
    ONE = 'one'; ANY = 'any'; TWO = 'two'; NOT_ONE = 'not_one'
    if len(payment) == 1:
        key = ANY if random_number < 0.2 else ONE
    elif len(payment) == 2:
        key = random.choice([ANY, TWO, NOT_ONE])
    else:
        key = ANY if random_number < 0.75 else NOT_ONE
    if not is_bargain:
        population, weights = GROUPS_BY_PAYMENT_LEN[key]
        return_type = random.choices(population, weights=weights)[0]
    else:
        return_type = ReturnType.RANDOM_NUMS
    return TradeM(Trade(payment, return_type, multiplier), amount)
