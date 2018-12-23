import requests
from monitors import stub, cpu_temp
import db_deets
from DatabaseTools import DatabaseTools

db = DatabaseTools()
ifttt_hook = 'https://maker.ifttt.com/trigger/%s/with/key/%s'

stub_top = 12
stub_bottom = 25
cpu_temp_top = 30.0
cpu_temp_bottom = 20.0


def send_request(name):
    request = ifttt_hook % (name, db_deets.ifttt_key)
    requests.post(request)


def run_update(func, top, bottom, *args):
    """

    Parameters
    ----------
    func : function_or_method
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
    variable = func.__name__
    val = func(*args)
    db.push_value(val, variable)
    if val > top:
        send_request(variable + '_above_max')
    elif val < bottom:
        send_request(variable + '_below_min')


try:
    run_update(stub, stub_top, stub_bottom, 12)
    run_update(cpu_temp, cpu_temp_top, cpu_temp_bottom)
except:
    send_request('cataclysm_occurred')
    raise
    



