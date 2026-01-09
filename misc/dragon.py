from turtle import Turtle, Screen, mainloop, pencolor
from math import sqrt
from itertools import tee

# L-system set up

START = "f"
RULES = {"f": "f+g", "g": "f-g"}
# START = "Fa"
# RULES = {"a": "aRbFR", "b": "LFaLb"}

LEVEL = 10
TARGET = 500

LINE = 15
ANGLE = 90
CIRCLE = LINE // 6
CURVE = LINE // 5

# string = START
# for _ in range(LEVEL):
#     string = "".join(RULES.get(character, character) for character in string)


CACHE = {}


# def expand(string, depth):
#     if (string, depth) not in CACHE:
#         final = ""
#         for char in string:
#             if char in RULES and depth < LEVEL:
#                 substring = expand(RULES[char], depth + 1)
#                 final += substring
#             else:
#                 final += char
#         CACHE[(string, depth)] = final
#     return CACHE[(string, depth)]


def expand(string, depth=0):
    if (string, depth) not in CACHE:
        final = ""
        for char in string:
            if char in RULES and depth < LEVEL:
                sbs1, sbs2 = tee(expand(RULES[char], depth + 1), 2)
                final += "".join(sbs1)
                yield from sbs2
            else:
                final += char
                yield char
        CACHE[(string, depth)] = final
    else:
        yield from CACHE[(string, depth)]


UP = 0
LEFT = 90
DOWN = 180
RIGHT = 270


string = expand(START)
# print("".join(string))
# print(string)

screen = Screen()
screen.tracer(False)

# turtle initialization
turtle = Turtle(visible=False)
turtle.setheading(90)

# apply the RULES from text to graphics
turtle.pencolor(1, 0, 0)
steps = 0
for character in string:
    if character in ["+", "R"]:
        turtle.right(ANGLE // 2)
        turtle.forward(CURVE * sqrt(2))
        turtle.right(ANGLE // 2)
    elif character in ["-", "L"]:
        turtle.left(ANGLE // 2)
        turtle.forward(CURVE * sqrt(2))
        turtle.left(ANGLE // 2)
    elif character in ["f", "g", "F"]:
        turtle.forward(LINE - 2 * CURVE)
        steps += 1

        if steps == TARGET:
            turtle.fillcolor(1, 0, 0)
            turtle.penup()
            turtle.forward(CURVE)
            turtle.right(90)
            turtle.forward(CIRCLE)
            turtle.left(90)
            turtle.pendown()
            turtle.begin_fill()
            turtle.circle(CIRCLE)
            turtle.end_fill()
            turtle.penup()
            turtle.left(90)
            turtle.forward(CIRCLE)
            turtle.right(90)
            turtle.backward(CURVE)
            turtle.pencolor(0, 0, 0)
            turtle.pendown()


screen.update()


screen.tracer(True)
turtle.hideturtle()

mainloop()
