# ruff: noqa: N806

"""Compute day of the week for a given date using Zeller's Congruence"""
# https://en.wikipedia.org/wiki/Zeller%27s_congruence

WEEKDAYS = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


def compute_day_of_week(year: int, month: int, day: int) -> None:
    q = day
    m = (month + 12) if month <= 2 else month
    Y = (year - 1) if month <= 2 else year
    J, K = divmod(Y, 100)
    # print(q, m, K, J)

    h = (q + (13 * (m + 1)) // 5 + K + K // 4 + J // 4 + 5 * J) % 7
    h2 = (q + (13 * (m + 1)) // 5 + Y + Y // 4 - Y // 100 + Y // 400) % 7
    assert h == h2
    print(f"The day of the week for {year}-{month:02d}-{day:02d} is {WEEKDAYS[h]}.")


if __name__ == "__main__":
    input_date = input("Enter a date (YYYY-MM-DD): ")
    year, month, day = map(int, input_date.split("-"))
    compute_day_of_week(year, month, day)
