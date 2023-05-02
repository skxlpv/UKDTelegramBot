from datetime import datetime

import pytz

tz = pytz.timezone('Europe/Kiev')


def get_today_date(timezone=tz):
    today = datetime.now(timezone).date()
    return today
