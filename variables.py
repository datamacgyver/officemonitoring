from datetime import datetime
from ics import Calendar
import requests
import monitors as m
from logons import calendar_url


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
    'func': m.stub
}

cpu_temp = {
    'top': 50.0,
    'bottom': 20.0,
    'func': m.cpu_temp
}

room_temp = {
    'top': 19.0 if in_the_office else 5.0,
    'bottom': 3.0 if in_the_office else 16.0,
    'func': m.room_temp
}

room_humidity = {
    'top': 1.0 if in_the_office else 65.0,  # On if I'm in
    'bottom': 0.0,
    'func': m.room_humidity
}

if __name__ == "__main__":
    print(stub)
    print(cpu_temp)
    print(room_temp)
    print(room_humidity)
