"""
This module simply contains calls to my IFTTT account that pushes
notifications to my phone this way I can know when things change
(or more likely crash)
"""

import requests
from secure.logons import ifttt_key

IFTTT_HOOK = 'https://maker.ifttt.com/trigger/%s/with/key/%s'


def action_notification(name='office_environment', variable=None, reading=None):
    json = {
        'value1': variable,
        'value2': reading
    }

    request = IFTTT_HOOK % (name, ifttt_key)
    requests.post(request, json=json, verify=False)


def error_notification(name='cataclysm_occurred', msg=None):
    json = {
        'value1': msg
    }

    request = IFTTT_HOOK % (name, ifttt_key)
    requests.post(request, json=json, verify=False)


if __name__ == "__main__":
    action_notification(variable='stub', reading=100)
    error_notification(msg='test')
