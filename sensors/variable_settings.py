from connectors.google_calendar import check_in_office
from sensors import variable_sensors as m

in_the_office = check_in_office()


stub = {
    'upper': 12.0,
    'lower': 25.0,
    'func': m.stub,
    'above_action': None,
    'below_action': None,
    'minutes_to_wait': 0,
    'record_outcome': 'always'
}

cpu_temp = {
    'upper': 55.0,
    'lower': 5.0,
    'func': m.cpu_temp,
    'above_action': None,
    'below_action': None,
    'minutes_to_wait': 15,
    'record_outcome': 'always'
}

room_temp = {
    'upper': 60.0,
    'lower': 17.0 if in_the_office else 3.0,
    'func': m.room_temp,
    'below_action': 'boost shed heater',
    'above_action': None,
    'minutes_to_wait': 15,
    'record_outcome': 'always'
}

# room_humidity = {
#     'upper': 50.0 if in_the_office else 75.0,
#     'lower': 0.0,
#     'func': m.room_humidity,
#     'below_action': None,
#     'above_action': 'shed humidifier on',
#     'minutes_to_wait': 15,
#     'record_outcome': 'always'
# }

room_motion = {
    'upper': 1.0,
    'lower': 0.0,
    'func': m.motion,
    'below_action': None,
    'above_action': 'shed lights on',
    'minutes_to_wait': 0,
    'record_outcome': 'if true'
}


if __name__ == "__main__":
    print(stub)
    print(cpu_temp)
    print(room_temp)
    # print(room_humidity)
