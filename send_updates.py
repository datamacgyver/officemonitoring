import requests
import monitors
import db_deets
import limits
import urllib.parse as parse
from DatabaseTools import DatabaseTools

ifttt_hook = 'https://maker.ifttt.com/trigger/%s/with/key/%s'


def send_request(name, json=None):
    request = ifttt_hook % (name, db_deets.ifttt_key)
    # print(request)
    requests.post(request, json=json)


def run_update(variable, *args):
    """

    Parameters
    ----------
    variable : Str
        function to call to get new value
    args : args
        additional arguments to pass to func

    Returns
    -------
    None

    """
    func = getattr(monitors, variable)
    limit = getattr(limits, variable)  # TODO: bundle with the above?
    val = func(*args)
    db.push_value(val, variable)
    if val > limit['top']:
        send_request(variable + '_above_max')
    elif val < limit['bottom']:
        send_request(variable + '_below_min')


try:
    db = DatabaseTools()
    run_update('stub')
    run_update('cpu_temp')
    run_update('room_temp')
    run_update('room_humidity')
except Exception as E:
    send_request('cataclysm_occurred',
                 json={'Value1': parse.quote_plus(str(E))})
    print('Cataclysmic error occurred. Reported to IFTTT')
    raise
