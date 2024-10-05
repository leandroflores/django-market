import random
import string

from datetime import date, datetime, timezone

def to_date(str_date: str, format: str = "%Y-%m-%d") -> date:
    try:
        return datetime.strptime(str_date, format).date()
    except Exception:
        return None

def random_numbers(size: int = 10) -> str:
    return "".join(
        random.choices(
            string.digits, 
            k=size)
        )

def random_str(size: int = 10) -> str:
    return "".join(
        random.choices(
            string.ascii_letters, 
            k=size)
        )

def random_int(min: int = 0, max: int = 1000) -> int:
    return random.randint(min, max)

def today() -> date:
    return datetime.now(timezone.utc).date()

def today_datetime() -> datetime:
    return datetime.now(timezone.utc)
