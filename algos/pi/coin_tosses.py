# https://www.youtube.com/watch?v=kahGSss6SsU

# Flip coins repeatedly, split into runs where tails are more common than heads
# Once there is more heads than tails, end the run, and note the ratio.
# This ratio appraoches 1/2 * arcsin(1) = pi / 4.

import random


def estimate_pi(num_tosses):
    heads_count = 0
    run_length = 0
    ratio_sum = 0
    runs = 0

    for _ in range(num_tosses):
        is_heads = random.random() < 0.5
        run_length += 1
        if is_heads:
            heads_count += 1
        # print("H" if is_heads else "T", end="")

        ratio = heads_count / run_length
        if ratio > 0.5:
            heads_count = 0
            run_length = 0
            ratio_sum += ratio
            runs += 1
            # print("  -> Ratio:", ratio)
    # print()

    return ratio_sum / runs * 4


# Up to ~3.13
for tosses in [100, 1e3, 1e5, 1e6, 1e7, 1e8]:
    print(f"Tosses: {int(tosses)}, Estimated Pi: {estimate_pi(int(tosses))}")
