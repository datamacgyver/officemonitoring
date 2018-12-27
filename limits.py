from datetime import datetime

day_start = 6
day_end = 18

now = int(datetime.strftime(datetime.now(), '%H'))
is_day = (now >= day_start) and (now <= day_end)

stub = {
    'top': 12.0,
    'bottom': 25.0
}

cpu_temp = {
    'top': 50.0,
    'bottom': 20.0
}

room_temp = {
    'top': 19.0 if is_day else 5.0,
    'bottom': 3.0 if is_day else 16.0
}

room_humidity = {
    'top': 1.0 if is_day else 65.0,  # On if I'm in
    'bottom': 0.0
}

if __name__ == "__main__":
    print(room_temp)
