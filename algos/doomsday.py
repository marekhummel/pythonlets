"""Computes the day of the week for any given date using the Doomsday algorithm."""

WEEKDAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


def compute_doomsday(year: int, month: int, day: int) -> None:
    anchor_day = _anchorday_of_century(year)
    doomsday = _doomsday_of_year(year, anchor_day)
    distance = _find_closest_anchor_day(month, day, doomsday)
    day_of_week = _compute_day_of_week_from_distance(doomsday, distance)

    print("===========================================")
    print(f"{year}-{month:02}-{day:02} falls on a {WEEKDAYS[day_of_week]}.")


def _anchorday_of_century(year: int) -> int:
    print("Step 01: Calculate the century's anchor day")
    print("-------------------------------------------")
    print("Remember that the anchor days for centuries are:")
    print("1700s = Tuesday (2), 1800s = Sunday (0), 1900s = Friday (5), 2000s = Wednesday (3)")
    print("Repeating every 400 years, so 2100s = Tuesday (2), etc.")
    print(f"Thus, {year} is in the {year // 100}00s century, so its anchor day is: ")

    anchor_day = [2, 0, 5, 3][(year // 100) % 4]
    print(f"  {WEEKDAYS[anchor_day]} ({anchor_day})")
    print()
    return anchor_day


def _doomsday_of_year(year: int, anchor_day: int) -> int:
    print("Step 02: Calculate the year's doomsday")
    print("-------------------------------------------")
    year_in_century = year % 100
    print(f"Take the last two digits of the year: {year} -> {year_in_century}")
    print("Divide by 12 and note the quotient and remainder:")
    div_12 = year_in_century // 12
    rem_12 = year_in_century % 12
    print(f"  {year_in_century} / 12 = {div_12} with a remainder of {rem_12}")
    print("Now divide the remainder by 4 (this is for the leap years), ignore the remainder:")
    div_4 = rem_12 // 4
    print(f"  {rem_12} / 4 = {div_4}")
    total = div_12 + rem_12 + div_4
    print(f"Sum these three numbers: {div_12} + {rem_12} + {div_4} = {total}")
    print(f"Now add the century's anchor day: {total} + {anchor_day} = {total + anchor_day}")
    doomsday = (total + anchor_day) % 7
    print("Finally, take this sum modulo 7 to get the year's doomsday:")
    print(f"  {WEEKDAYS[doomsday]} ({doomsday})")
    print(
        f"This means that in this year, the following dates all fall on a {WEEKDAYS[doomsday]}:\n"
        "  4/4, 6/6, 8/8, 10/10, 12/12,\n"
        "  9/5, 5/9, 7/11, 11/7,\n"
        "  Either 3/1 or 4/1 (in leap years),\n"
        "  The last day of February (either 28/2 or 29/2),\n"
        "  Pi Day (14/3), Boxing Day (26/12), Halloween (31/10), Day of German Unity (3/10)"
    )
    print()
    return doomsday


def _find_closest_anchor_day(month: int, day: int, doomsday: int) -> int:
    print("Step 03: Find the closest doomsday date to the given date")
    print("-------------------------------------------")

    is_leap = False
    if month in [1, 2]:
        print("Since its January or February, first determine if it's a leap year.")
        print("A year is a leap year if it is divisible by 4, except for end-of-century years,")
        print("which must be divisible by 400 to be leap years.")
        print(f"  {year} % 4 = {year % 4}")
        if year % 4 == 0:
            if (year % 100 == 0) and (year % 400 != 0):
                print(
                    "Even though it's divisible by 4, it's an end-of-century year not "
                    "divisible by 400, so not a leap year."
                )
            else:
                print("It's a leap year.")
        else:
            print("It's not a leap year.")

        is_leap = year % 4 == 0 and not ((year % 100 == 0) and (year % 400 != 0))

    month_anchors = {
        1: ([3], [4]),
        2: ([28], [29]),
        3: ([14],),
        4: ([4],),
        5: ([9],),
        6: ([6],),
        7: ([11],),
        8: ([8],),
        9: ([5],),
        10: ([3, 10, 31],),
        11: ([7],),
        12: ([12, 26],),
    }
    options = month_anchors[month][1 if is_leap else 0]
    print(
        f"Given the month is {month}, known {WEEKDAYS[doomsday]}s are: "
        "  " + ", ".join(f"{d}/{month}" for d in options)
    )
    closest_date = next((d for d in sorted(options) if d >= day), options[0])
    print(
        f"The closest doomsday date to {day}/{month} is {closest_date}/{month}, "
        f"with a distance of {day - closest_date} days."
    )
    print()

    return day - closest_date


def _compute_day_of_week_from_distance(doomsday: int, distance: int) -> int:
    print("Step 04: Compute the day of the week from the distance")
    print("-------------------------------------------")
    print(f"Given that your date is {distance} days from the doomsday {doomsday}, add them:")
    day_of_week = doomsday + distance
    print(f"  {doomsday} + {distance} = {day_of_week}")
    if day_of_week < 0:
        print("Since this is negative, keep adding 7 until you get a positive number.")
        additions = day_of_week // 7 * -1 + 1
        print(f"  {day_of_week} " + ("+ 7" * additions) + f" = {day_of_week + 7 * additions}")
        day_of_week += 7 * additions

    print("Lastly, find the result modulo 7 to get the final day of the week:")
    print(", ".join(f"{i} = {wd}" for i, wd in enumerate(WEEKDAYS)))
    print()

    return day_of_week % 7


if __name__ == "__main__":
    input_date = input("Enter a date (YYYY-MM-DD): ")
    year, month, day = map(int, input_date.split("-"))
    compute_doomsday(year, month, day)
