from itertools import count
from math import sqrt
from typing import Iterator, List, Tuple


def euler_totient_sieve(n: int) -> List[int]:
    """Combines sieve of eratostenes and euler totient function"""
    phi = [i for i in range(n + 1)]
    for p in range(2, n + 1):
        if phi[p] == p:
            # means we found a prime
            phi[p] = p - 1

            # update multiples as they have p as their prime factor
            for mp in range(2 * p, n + 1, p):
                phi[mp] = (phi[mp] // p) * (p - 1)

    return phi


def prime_sieve_eratostenes(n):
    """Sieve of Eratostenes up to n"""
    root = int(sqrt(n))
    primes = [True] * (n + 1)
    primes[0:2] = [False, False]
    for i in range(2, root + 1):
        if primes[i]:
            m = n // i - i + 1
            primes[i * i : n + 1 : i] = [False] * m

    return (i for i, p in enumerate(primes) if p)


def prime_sieve_atkins(limit: int):
    """Sieve of Atkins up to n"""
    is_prime = [False] * limit
    s = [1, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59]

    n_mod_60_1 = {1, 13, 17, 29, 37, 41, 49, 53}
    for x in count(1):
        x2 = 4 * x * x
        if x2 >= limit:
            break
        for y in count(1, step=2):
            n = x2 + y * y
            if n >= limit:
                break
            if n % 60 in n_mod_60_1:
                is_prime[n] = not is_prime[n]

    n_mod_60_2 = {7, 19, 31, 43}
    for x in count(1, step=2):
        x2 = 3 * x * x
        if x2 >= limit:
            break
        for y in count(2, step=2):
            n = x2 + y * y
            if n >= limit:
                break
            if n % 60 in n_mod_60_2:
                is_prime[n] = not is_prime[n]

    n_mod_60_3 = {11, 23, 47, 59}
    for x in count(2, step=1):
        x2 = 3 * x * x
        if 2 * x * x + 2 * x - 1 >= limit:
            break
        for y in range(x - 1, 0, -2):
            n = x2 - y * y
            if n >= limit:
                break
            if n % 60 in n_mod_60_3:
                is_prime[n] = not is_prime[n]

    for w in count(0):
        if 3600 * w * w >= limit:
            break
        for x in s:
            n = 60 * w + x
            if n < 7:
                continue

            n2 = n * n
            if n2 >= limit:
                break

            if is_prime[n]:
                for w2 in count(0):
                    if n2 * (60 * w2 * s[0]) >= limit:
                        break
                    for x2 in s:
                        c = n2 * (60 * w2 + x2)
                        if c >= limit:
                            break

                        is_prime[c] = False

    yield from [2, 3, 5]
    for w in count(0):
        if 60 * w >= limit:
            break
        for x in s:
            n = 60 * w + x
            if n < 7:
                continue
            if n > limit:
                break
            if is_prime[n]:
                yield n


def naive_is_prime(n: int) -> bool:
    """Checks if integer n is prime"""
    if n % 2 == 0:
        return n == 2

    for f in range(3, int(sqrt(n)) + 1, 2):
        if n % f == 0:
            return False

    return n > 1


def is_prime(n):
    """Primality test with miller rabin. Due to the given values of a, this
    is still fully deterministic. Note that this method returns True if the
    input is prime (contrary to the original miller rabin)"""
    if n & 1 == 0 or n <= 3:
        return n in [2, 3]

    # Find u and k, so that n-1 = u * 2**k
    u, k = n - 1, 0
    while u & 1 == 0:
        u >>= 1
        k += 1

    # Choices for a
    for a in _get_miller_rabin_a_list(n):
        if a > n - 1:
            break

        # b_0
        b = pow(a, u, n)
        if b in [1, n - 1]:
            continue  # A-Liar

        # b_i with i = 1...k
        for _ in range(k):
            b = pow(b, 2, n)
            if b == n - 1:
                break  # A-Liar
            if b == 1:
                return False  # A-Witness
        else:
            return False  # F-Witness

    # Research showed that if all a were A-Liars, n is definitely prime
    return True


def _get_miller_rabin_a_list(n):
    if n < 2_047:
        return [2]
    if n < 1_373_653:
        return [2, 3]
    if n < 9_080_191:
        return [31, 73]
    if n < 4_759_123_141:
        return [2, 7, 61]
    if n < 2_152_302_898_747:
        return [2, 3, 5, 7, 11]
    if n < 3_474_749_660_383:
        return [2, 3, 5, 7, 11, 13]
    if n < 341_550_071_728_321:
        return [2, 3, 5, 7, 11, 13, 17]
    if n < 3_825_123_056_546_413_051:
        return [2, 3, 5, 7, 11, 13, 17, 19, 23]
    if n < 318_665_857_834_031_151_167_461:
        return [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    return None


def prime_factors(n: int) -> Iterator[Tuple[int, int]]:
    """Computes prime factors of n as a list of tuples (p_i, k_i),
    so that n = prod(p_i**k_i)"""
    p = 2
    while p * p <= n:
        k = 0
        while n % p == 0:
            n //= p
            k += 1

        if k != 0:
            yield p, k

        if n == 1:
            break

        p += 1 if p == 2 else 2
    if n > 1:
        yield n, 1


if __name__ == "__main__":
    n = 10000
    primes1 = prime_sieve_eratostenes(n)
    primes2 = prime_sieve_atkins(n)
    assert set(primes1) == set(primes2)
