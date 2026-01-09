# Linear Feedback Shift Register
# https://www.youtube.com/watch?v=Ks1pw1X22y4


def lsfr(input_str, feedback_func):
    n = len(input_str)

    def one_iter(val):
        feedback = feedback_func(val)
        new = (feedback << (n - 1)) | (val >> 1)
        return new

    start = int(input_str, 2)
    state = start
    i = 1
    out = ""
    while (state != start or i == 1) and i < 10000:
        # print(state & 1, end='')
        out += str(state & 1)
        state = one_iter(state)
        # print(i, f'{state:0{n}b}')
        i += 1

    return out


def feedback(s):
    return (s ^ (s >> 1)) & 1


def feedback2(s):
    return ((s >> 0) ^ (s >> 1) ^ (s >> 3)) & 1


def feedback3(s):
    return ((s >> 0) ^ (s >> 1) ^ (s >> 2) ^ (s >> 7)) & 1


start = f"{(1 << 127) | 1:0b}"
print(start)
out = lsfr(start, feedback3)
print(out)
