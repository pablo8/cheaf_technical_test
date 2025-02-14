from datetime import datetime

import pytz
from dateutil.relativedelta import relativedelta


def convert_str_to_datetime(s):
    """
    Convert str to datetime.

    :param s: str, ex: "31/12/2020 12:40" or "31/12/20 12:40"
    :return: datetime or None if parsing fails
    """
    for fmt in ("%d/%m/%Y %H:%M", "%d/%m/%y %H:%M"):
        try:
            return datetime.strptime(s, fmt).astimezone(pytz.UTC)
        except ValueError:
            continue
    return None


def calculate_activation_dates(expiration_date):
    try:
        return expiration_date - relativedelta(days=10), expiration_date - relativedelta(days=5)
    except:
        return None, None


def output_date_format(_datetime):
    try:
        return datetime.strftime(_datetime, '%d/%m/%Y %H:%M')
    except:
        return None


def get_start_end_dates(range_dates):
    date_list = range_dates.split(',')
    date_start = datetime.strptime(date_list[0], "%Y-%m-%d").date()
    date_end = datetime.strptime(date_list[1], "%Y-%m-%d").date()
    return date_start, date_end
