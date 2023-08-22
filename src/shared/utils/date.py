from datetime import datetime


def todays_date() -> str:
    return datetime.now().strftime("%d-%m-%Y")
