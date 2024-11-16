# Monte-Carlo exp on monopoly game to compute probabilities of each square

import random

rolls = 1000000
spaces = [0] * 40
curr = 0
doubles = 0

# fmt: off
dice = [i + j for j in range(1, 7) for i in range(1, 7)]
communities = [0, 10] + [-1] * 14
chances = [0, 24, 11, "UTILITY", "RAILROAD", "RAILROAD", -1, "BACK", 10, -1, -1, 5, 39, -1, -1, -1]  # noqa
# fmt: on
random.shuffle(communities)
random.shuffle(chances)

for i in range(0, rolls):
    index = random.randint(0, len(dice) - 1)

    doubles = doubles + 1 if index in [0, 7, 14, 21, 28, 35] else 0
    if doubles == 3:
        doubles = 0
        curr = 10
    else:
        steps = dice[index]
        curr = (curr + steps) % 40

        # Community Chest
        if curr in [2, 17, 33]:
            card = communities.pop(0)
            if card != -1:
                curr = card
            communities.append(card)

        # Chances
        if curr in [7, 22, 36]:
            card = chances.pop(0)
            if card in [0, 10, 5, 11, 24, 39]:
                curr = card
            elif card == "BACK":
                curr -= 3
                if curr < 0:
                    curr += 40
            elif card == "UTILITY":
                while curr not in [12, 28]:
                    curr = (curr + 1) % 40
            elif card == "RAILWAY":
                while curr not in [5, 15, 25, 35]:
                    curr = (curr + 1) % 40
            chances.append(card)

        # GO TO JAIL
        if curr == 30:
            curr = 10

    spaces[curr] += 1


probs = [[i, round(c / rolls * 100, 2)] for i, c in enumerate(spaces)]
probs = sorted(probs, key=lambda p: p[1], reverse=True)
ranking = zip(range(1, 41), probs)

# pos, square index, prob
print(*ranking, sep="\n")
# input()
