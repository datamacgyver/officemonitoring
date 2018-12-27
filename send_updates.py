import requests
import monitors
import db_deets
import urllib.parse as parse
from DatabaseTools import DatabaseTools

ifttt_hook = 'https://maker.ifttt.com/trigger/%s/with/key/%s'

stub_top = 12
stub_bottom = 25
cpu_temp_top = 50.0
cpu_temp_bottom = 20.0
room_temp_top = 5.0
room_temp_bottom = 3.0  # TODO: This needs to be altered based on me being there
room_humidity_top = 70.0
room_humidity_bottom = 0.0


def send_request(name, json=None):
    request = ifttt_hook % (name, db_deets.ifttt_key)
    # print(request)
    requests.post(request, json=json)


def run_update(variable, top, bottom, *args):
    """

    Parameters
    ----------
    variable : Str
        function to call to get new value
    top : float
        max return value before posting to exceeded webhook
    bottom : float
        min return value before posting to lower webhook
    args : args
        additional arguments to pass to func

    Returns
    -------
    None

    """
    func = getattr(monitors, variable)
    val = func(*args)
    db.push_value(val, variable)
    if val > top:
        send_request(variable + '_above_max')
    elif val < bottom:
        send_request(variable + '_below_min')


try:
    db = DatabaseTools()
    run_update('stub', stub_top, stub_bottom)
    run_update('cpu_temp', cpu_temp_top, cpu_temp_bottom)
    run_update('room_temp', room_temp_top, room_temp_bottom)
    run_update('room_humidity', room_humidity_top, room_humidity_bottom)
except Exception as E:
    send_request('cataclysm_occurred',
                 json={'Value1': parse.quote_plus(str(E))})
    print('Cataclysmic error occurred. Reported to IFTTT')
    raise
