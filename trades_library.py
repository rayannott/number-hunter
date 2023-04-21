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
    cum_difficulty += 0.15 * len(payment)
    multiplier = max(1, round(cum_difficulty * 5))
    population_key, weights_key = 'any', 'any_weights' if len(payment) != 1 or random.random() < 0.5 else 'one', 'one_weights'
    return_type = random.choices(GROUPS_BY_PAYMENT_LEN[population_key], weights=GROUPS_BY_PAYMENT_LEN[weights_key])[0]
    return TradeM(Trade(payment, return_type, multiplier), amount)
