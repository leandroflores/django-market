from datetime import date, datetime, timezone
from market import utils

def test_to_date():

    # Arrange
    year: int = 2024
    month: int = 10
    day: int = 12
    str_date: str = "2024-08-10"

    # Act
    _date: date = utils.to_date(f"{year}-{month}-{day}")

    # Assert
    assert _date == date(year, month, day)

def test_random_numbers():

    # Act
    numbers: str = utils.random_numbers()

    # Assert
    assert len(numbers) == 10
    assert type(numbers) == str
    assert numbers.isdigit() == True

def test_random_str():

    # Act
    string: str = utils.random_str()

    # Assert
    assert len(string) == 10
    assert type(string) == str
    assert string.isalpha() == True

def test_random_int():

    # Act
    number: int = utils.random_int()

    # Assert
    assert number in range(0, 1000)
    assert type(number) == int

def test_today():

    # Act
    today: date = utils.today()

    # Assert
    assert type(today) == date
    assert today == datetime.now(timezone.utc).date()

def test_today_datetime():

    # Act
    today: datetime = utils.today_datetime()

    # Assert
    assert type(today) == datetime
    assert today.date() == datetime.now(timezone.utc).date()
