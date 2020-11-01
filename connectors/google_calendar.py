from datetime import datetime

CALENDAR_FILE = 'GoogleCalendar.pickle'
NOW_HR = datetime.now().strftime("%Y%m%d%H")
NOW_DAY = datetime.now().strftime("%Y%m%d")


def _get_calendar():
    """
    Once a day, download my works calender. Cache it for further
    calls that day
    """
    # Imports here as we don't want to slow down the regular updates.
    from ics import Calendar
    from secure.logons import calendar_url
    from pickle import load, dump
    from requests import get

    # Read last cache
    try:
        with open(CALENDAR_FILE, 'rb') as f:
            c = load(f)
    except(FileNotFoundError, EOFError):
        c = (0, None)
    write_date = c[0]
    calendar = c[1]

    # Check if an update is needed
    if int(write_date) != int(NOW_DAY):
        print('Refreshing calendar')
        calendar = get(calendar_url).text
        with open(CALENDAR_FILE, 'wb') as f:
            c = (NOW_DAY, calendar)
            dump(c, f)
    else:
        print('Using cached calendar')

    return Calendar(calendar)


def check_in_office(day_start_hr=6, day_end_hr=17, weekday_start=0, weekday_end=4):
    """
    Basically, check it's not a weekend and also check my works calender
    to see if I'm in London.
    """
    # See if we already checked this hour
    filename = 'office_check.txt'
    try:
        with open(filename, 'r') as f:
            check = f.readlines()
            print(check)
        if check[0] == str(NOW_HR) + '\n':
            return check[1] == 'True'
    except FileNotFoundError:
        pass

    c = _get_calendar()

    hour_now = int(datetime.strftime(datetime.now(), '%H'))
    weekday_now = datetime.today().weekday()
    date_now = datetime.today().date()

    in_london = any([event.begin.date() == date_now for event in c.events])
    is_day = (hour_now >= day_start_hr) and (hour_now <= day_end_hr)
    is_week = (weekday_now <= weekday_end) and (weekday_now >= weekday_start)

    check_result = is_day and is_week and not in_london
    print("Is rob in his office? %s" % check_result)

    with open(filename, 'w') as f:
        f.writelines(NOW_HR + '\n' + str(check_result))

    return check_result


if __name__ == '__main__':
    print(check_in_office())
