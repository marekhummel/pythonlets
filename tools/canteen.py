from dataclasses import dataclass
import requests
from dacite import from_dict

BASE_URI = "https://openmensa.org/api/v2/"
KIEL = (54.3385681, 10.1341526)


@dataclass
class Canteen:
    id: int
    name: str
    city: str
    address: str
    coordinates: list[float]


@dataclass
class Day:
    date: str
    closed: bool


@dataclass
class Prices:
    students: float | None
    employees: float | None
    pupils: float | None
    others: float | None


@dataclass
class Meal:
    id: int
    name: str
    category: str
    prices: Prices
    notes: list[str]


def get_canteens() -> list[Canteen] | None:
    uri = BASE_URI + "/canteens"
    params = {
        "near[lat]": KIEL[0],
        "near[lng]": KIEL[1],
        "near[dist]": 10,
    }

    resp = requests.get(uri, params=params)
    if resp.status_code != 200:
        print(f"Resp error: {resp.status_code}")
        return None

    data = [from_dict(Canteen, obj) for obj in resp.json()]
    return data


def get_days(id: int) -> list[Day] | None:
    uri = BASE_URI + f"/canteens/{id}/days"
    resp = requests.get(uri)
    if resp.status_code != 200:
        print(f"Resp error: {resp.status_code}")
        return None

    data = [from_dict(Day, obj) for obj in resp.json()]
    return data


def get_meals(id: int, date: str) -> list[Meal] | None:
    uri = BASE_URI + f"/canteens/{id}/days/{date}/meals"
    resp = requests.get(uri)
    if resp.status_code != 200:
        print(f"Resp error: {resp.status_code}")
        return None

    data = [from_dict(Meal, obj) for obj in resp.json()]
    return data


if __name__ == "__main__":
    canteens = get_canteens()
    assert canteens
    print([c.name for c in canteens])

    mensa_i = next(c for c in canteens if c.name == "Mensa I")
    days = get_days(mensa_i.id)
    assert days
    print(days)

    day = days[0]
    meals = get_meals(mensa_i.id, day.date)
    assert meals
    print()
    for meal in meals:
        print("- ", meal.name)
