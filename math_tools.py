import random
from math import log, sqrt

from utils import N


def is_prime(n: int) -> bool:
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n < 2:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def get_primes_up_to():
    return [el for el in range(N) if is_prime(el)]


PRIMES_UP_TO_N = get_primes_up_to()


def random_prime() -> int:
    return random.choice(PRIMES_UP_TO_N)


def is_perfect_square(n: int) -> bool:
    return round(n**0.5) ** 2 == n


def is_perfect_power(n: int) -> bool:
    for base in range(2, int(sqrt(n)) + 1):
        for power in range(2, int(log(n, base)) + 1):
            if base**power == n:
                return True
    return False


def is_power_of_two(n: int) -> bool:
    return 2 ** round(log(n, 2)) == n


def closest_prime(n: int) -> int:
    if is_prime(n):
        return n
    below = None
    above = None
    for i in range(n):
        if below is None and is_prime(n - i):
            below = n - i
            if 0 <= below < N:
                return below
        if above is None and is_prime(n + i):
            above = n + i
            if 0 <= above < N:
                return above
    raise ValueError("No prime found")


def all_prime_factors(n: int) -> list[int]:
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


def digitize(n: int) -> list[int]:
    return [int(d) for d in str(n)]
