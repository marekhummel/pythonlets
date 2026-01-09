# https://www.youtube.com/watch?v=cbGB__V8MNk
# Compute large modulus exponentiations with square-and-multiply


def compute_chain(exponent):
    binary = f"{exponent:b}"
    chain = ""
    for bit in binary[1:]:
        chain += "S"
        if bit == "1":
            chain += "M"
    return chain


def execute_chain(base, chain, modulus):
    value = base
    for action in chain:
        if action == "S":
            value = value * value % modulus
        elif action == "M":
            value = value * base % modulus
    return value


# <n> ** <exponent> mod <modulus>
n = 23
exponent = 373
modulus = 747

chain = compute_chain(exponent)
print(execute_chain(n, chain, modulus), chain)
print(pow(n, exponent, modulus))
