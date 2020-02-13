from datetime import datetime

cal_file = 'GoogleCalendar.pickle'
NOW = datetime.now().strftime("%Y%m%d")


def get_calendar():
    from ics import Calendar
    from secure.logons import calendar_url
    from pickle import load, dump
    from requests import get

    # Read last cache
    try:
        with open(cal_file, 'rb') as f:
            c = load(f)
    except(FileNotFoundError, EOFError):
        c = (0, None)
    write_date = c[0]
    calendar = c[1]

    # Check if an update is needed
    if int(write_date) != int(NOW):
        print('Refreshing calendar')
        calendar = get(calendar_url).text
        with open(cal_file, 'wb') as f:
            c = (NOW, calendar)
            dump(c, f)
    else:
        print('Using cached calendar')

    return Calendar(calendar)


def check_in_office(day_start=6, day_end=17, weekday_start=0, weekday_end=4):
    # See if we already checked this
    filename = 'office_check.txt'
    try:
        with open(filename, 'r') as f:
            check = f.readlines()
            print(check)
        if check[0] == str(NOW)+'\n':
            return check[1] == 'True'
    except FileNotFoundError:
        pass

    c = get_calendar()

    hour_now = int(datetime.strftime(datetime.now(), '%H'))
    weekday_now = datetime.today().weekday()
    date_now = datetime.today().date()

    in_london = any([event.begin.date() == date_now for event in c.events])
    is_day = (hour_now >= day_start) and (hour_now <= day_end)
    is_week = (weekday_now <= weekday_end) and (weekday_now >= weekday_start)

    check_result = is_day and is_week and not in_london
    print("Is rob in his office? %s" % check_result)

    with open(filename, 'w') as f:
        f.writelines(NOW+'\n'+str(check_result))

    return check_result


if __name__ == '__main__':
    print(check_in_office())
