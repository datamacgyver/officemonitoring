import requests as r
import db_deets as db
import json

HEADER = {
    'content-type': 'application/json'
}


def get_access_token():

    # body = json.loads('{ \
    #     "username": "%s",\
    #     "password": "%s",\
    #     "devices": true,\
    #     "products": true,\
    #     "actions": true,\
    #     "homes": true,\
    # }' % (db.hive_user, db.hive_password))

    body = json.dumps({
        "username": db.hive_user,
        "password": db.hive_password,
        "devices": True,
        "products": True,
        "actions": True,
        "homes": True,
    })

    s = r.Session()
    req = r.Request('POST',
                    'https://beekeeper.hivehome.com/1.0/global/login',
                    json=str(body))  # json = body) # data=str(body))
    prepped = req.prepare()
    for key in list(prepped.headers.keys()):
        del prepped.headers[key]

    prepped.headers['Content-Type'] = 'application/json'
    resp = s.send(prepped, verify=False)

    print(resp.text)
    print(resp.request.body)
    print(resp.request.headers)

    input('WAITING')


    resp = json.loads(resp.text)
    return resp['token']



def logout(token):
    resp = requests.delete('https://beekeeper-uk.hivehome.com/1.0/auth/logout',
                           headers=HEADER, auth=token, verify=False)
    print(str(resp))


class HiveControls:

    def __init__(self):
        self.token = get_access_token()

    def __del__(self):
        logout(self.token)


token = get_access_token()
print(token)
logout(token)
