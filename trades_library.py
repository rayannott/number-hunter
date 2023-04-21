import random

from trades import Trade, TradeM
from return_types import GROUPS_BY_PAYMENT_LEN
from payments_library import get_random_payment


PREDEFINED_TRADEMS = [

]

PREDEFINED_TRADEMS_WEIGHTS = [

]

assert len(PREDEFINED_TRADEMS) == len(PREDEFINED_TRADEMS_WEIGHTS)


def get_random_trade() -> TradeM:
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
    ONE = ('one', 'one_weights'); ANY = ('any', 'any_weights'); NOT_ONE = ('not_one', 'not_one_weights')
    if len(payment) == 1:
        population_key, weights_key = ONE if random_number < 0.8 else ANY
    else:
        population_key, weights_key = ANY if random_number < 0.5 else NOT_ONE 
    return_type = random.choices(GROUPS_BY_PAYMENT_LEN[population_key], weights=GROUPS_BY_PAYMENT_LEN[weights_key])[0]
    return TradeM(Trade(payment, return_type, multiplier), amount)
