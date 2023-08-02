# Computes fraction which is equal to value of input
# https://www.youtube.com/watch?v=7LKy3lrkTRA

EPS = 1e-17


def farey_algorithm(value):
    a = (0, 1)
    b = (1, 1)

    while True:
        x = (a[0] + b[0], a[1] + b[1])

        xval = x[0] / x[1]
        if abs(xval - value) < EPS:
            return x
        elif xval < value:
            a = x
        else:
            b = x


x = 0.336944434029
num, deno = farey_algorithm(x)
print(f"Farey:  {num} / {deno}\n")
print(f"Original:  {x}")
print(f"Approx:    {num / deno}")
print(f"EPS:       {EPS:.20f}".rstrip("0"))
print(f"Delta:     {x - num / deno}")
