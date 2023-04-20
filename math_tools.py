from math import log, sqrt


def is_prime(n: int) ->  bool:
    if n == 2 or n == 3: return True
    if n % 2 == 0 or n < 2: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False    
    return True


def is_perfect_square(n: int) -> bool:
    return round(n ** .5) ** 2 == n


def is_perfect_power(n: int) -> bool:
    for base in range(2, sqrt(n)+1):
        for power in range(2, int(log(n, base))+1):
            if base**power == n:
                return True
    return False

def is_power_of_two(n):
    return 2**round(log(n, 2)) == n
