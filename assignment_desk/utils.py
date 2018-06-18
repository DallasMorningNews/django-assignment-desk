# Imports from python.  # NOQA
from datetime import datetime
from datetime import timedelta


def get_latest_monday():
    current_date = datetime.now().date()
    return current_date - timedelta(days=current_date.weekday())


def get_next_sunday():
    current_date = datetime.now().date()
    start_of_week = current_date - timedelta(days=current_date.weekday())
    return start_of_week + timedelta(days=6)
