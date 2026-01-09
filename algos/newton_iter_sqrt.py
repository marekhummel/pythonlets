a = 123.0

# Heron
x = a
for _ in range(100):
    x = 0.5 * (x + a / x)

print(x, x * x, a)

# Optimization to avoid div
x = 1 / a
for _ in range(100):
    x = 0.5 * x * (3 - a * x * x)

print(a * x, (a * x) * (a * x), a)
