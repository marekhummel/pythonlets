# List of students with respective scores (higher = better)
# Task is to reward all of them, with two rules:
# 1. At least one reward for everybody
# 2. Compared to the adjacent students, the reward has to be higher (lower) if the score is higher (lower)


def min_rewards(scores):
    rewards = [1] * len(scores)

    for i in range(1, len(scores)):
        if scores[i - 1] < scores[i]:
            rewards[i] = rewards[i - 1] + 1

    for i in range(len(scores) - 2, -1, -1):
        if scores[i] > scores[i + 1]:
            rewards[i] = max(rewards[i], rewards[i + 1] + 1)

    return rewards


scores = [8, 4, 2, 1, 3, 5, 7, 9, 1]
print(scores)
print(min_rewards(scores))
