from datetime import datetime
import monitors as m
from ics import Calendar
import requests    # Alternative: use requests
from db_deets import calendar_url

day_start = 6  # am
day_end = 18  # pm

hour_now = int(datetime.strftime(datetime.now(), '%H'))
weekday_now = datetime.today().weekday()
date_now = datetime.today().date()
c = Calendar(requests.get(calendar_url).text)

in_london = any([event.begin.date() == date_now for event in c.events])
is_day = (hour_now >= day_start) and (hour_now <= day_end)
is_week = weekday_now < 5  # 0 is monday

in_the_office = is_day and is_week and not in_london

print("Is rob in his office? %s" % in_the_office)
# print("in_london %s" % in_london)
# print("is_day %s" % is_day)
# print("is_week %s" % is_week)



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
    print(room_temp)
