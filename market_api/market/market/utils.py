from datetime import date, datetime

def to_date(str_date: str, format: str = "%Y-%m-%d") -> date:
    try:
        return datetime.strptime(str_date, format).date()
    except Exception as e:
        print(e)
        return None
