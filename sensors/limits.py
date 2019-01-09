from datetime import datetime
import requests
from ics import Calendar

from secure.logons import calendar_url
from sensors import monitors as m


def check_in_office(day_start=6, day_end=18, weekday_start=0, weekday_end=4):
    c = Calendar(requests.get(calendar_url).text)

    hour_now = int(datetime.strftime(datetime.now(), '%H'))
    weekday_now = datetime.today().weekday()
    date_now = datetime.today().date()

    in_london = any([event.begin.date() == date_now for event in c.events])
    is_day = (hour_now >= day_start) and (hour_now <= day_end)
    is_week = (weekday_now <= weekday_end) and (weekday_now >= weekday_start)

    check_result = is_day and is_week and not in_london
    print("Is rob in his office? %s" % check_result)

    return check_result


in_the_office = check_in_office()


stub = {
    'top': 12.0,
    'bottom': 25.0,
    'func': m.stub,
    'above_action': None,
    'below_action': None
}

cpu_temp = {
    'top': 55.0,
    'bottom': 5.0,
    'func': m.cpu_temp,
    'above_action': None,
    'below_action': None
}

room_temp = {
    'top': 100.0,
    'bottom': 17.0 if in_the_office else 3.0,
    'func': m.room_temp,
    'below_action': 'shed heater on',
    'above_action': None
}

room_humidity = {
    'top': 50.0 if in_the_office else 65.0,
    'bottom': 0.0,
    'func': m.room_humidity,
    'below_action': None,
    'above_action': 'shed humidifier on'
}

if __name__ == "__main__":
    print(stub)
    print(cpu_temp)
    print(room_temp)
    print(room_humidity)
