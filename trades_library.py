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
    if len(payment) == 1:
        return_type = random.choices(GROUPS_BY_PAYMENT_LEN['one'], weights=GROUPS_BY_PAYMENT_LEN['one_weights'])[0]
    else:
        return_type = random.choices(GROUPS_BY_PAYMENT_LEN['any'], weights=GROUPS_BY_PAYMENT_LEN['any_weights'])[0]
    return TradeM(
        Trade(payment, return_type),
        amount
    )
