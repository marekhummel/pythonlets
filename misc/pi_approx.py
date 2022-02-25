# https://www.youtube.com/watch?v=RZBhSi_PwHU
from random import randint
import math


def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)


maxi = 10000000
coprimes = 0
for i in range(0, maxi):
    a = randint(1, 100)
    b = randint(1, 100)

    if gcd(a, b) == 1:
        coprimes += 1

    if (i % 200 == 0):
        print(i, end="\r")


empprob = coprimes / maxi
print("Iterations: {0}".format(maxi))
print("Coprimes: {0}".format(coprimes))
print("Emp. Probability: {0}".format(empprob))
print("PI Approx.: {0}".format(math.sqrt(6 / empprob)))


# input()
