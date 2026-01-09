def get_digit(n, idx):
    return (n // (10**idx)) % 10  # digit


def radix_sort_buckets(array):
    digit_idx = 0
    diff_from_zero = True
    while diff_from_zero:
        # Fill buckets
        buckets = [[] for _ in range(10)]
        diff_from_zero = False
        for n in array:
            d = get_digit(n, digit_idx)
            diff_from_zero = diff_from_zero or (d != 0)
            buckets[d].append(n)

        # Create new list
        array = [elem for bckt in buckets for elem in bckt]

        # Next digit
        digit_idx += 1

    return array


def radix_sort_counts(array):
    digit_idx = 0
    diff_from_zero = True
    while diff_from_zero:
        # Count digits
        prefix_sum = [0] * 10
        diff_from_zero = False
        for n in array:
            d = get_digit(n, digit_idx)
            diff_from_zero = diff_from_zero or (d != 0)
            prefix_sum[d] += 1

        # Convert counters to prefix sum
        for i in range(1, 10):
            prefix_sum[i] += prefix_sum[i - 1]

        # Create output list
        output = [0 for _ in range(len(array))]
        for i in range(len(array) - 1, -1, -1):
            n = array[i]
            d = get_digit(n, digit_idx)
            prefix_sum[d] -= 1
            ti = prefix_sum[d]
            output[ti] = n

        # Next digit
        digit_idx += 1
        array = output

    return array


l = [717, 26, 785, 636, 955, 572, 772, 304, 935, 395, 267, 65, 699, 350, 23, 660]
print(l)

print(radix_sort_buckets(l))
print(radix_sort_counts(l))
