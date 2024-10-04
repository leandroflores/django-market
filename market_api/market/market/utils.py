import random
import string

from datetime import date, datetime

def to_date(str_date: str, format: str = "%Y-%m-%d") -> date:
    try:
        return datetime.strptime(str_date, format).date()
    except Exception as e:
        print(e)
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

def today() -> date:
    return datetime.today().date()
