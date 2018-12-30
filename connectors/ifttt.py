import requests
from secure import logons

ifttt_hook = 'https://maker.ifttt.com/trigger/%s/with/key/%s'


def send_request(name, json=None):
    request = ifttt_hook % (name, logons.ifttt_key)
    # print(request)
    requests.post(request, json=json)
