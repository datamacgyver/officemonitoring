import requests
import db_deets as db
import json


def get_access_token():
    url = "http://beekeeper.hivehome.com/1.0/global/login"

    payload = "{\"username\": \"%s\", " \
              "\"password\": \"%s\", " \
              "\"devices\": true, " \
              "\"products\": true, " \
              "\"actions\": true, " \
              "\"homes\": true}" % (db.hive_user, db.hive_password)
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'Postman-Token': "1a8d9050-f7ae-4246-9afe-6dae9baddb2e"
    }

    response = requests.request("POST", url, data=payload,
                                headers=headers, verify=False)
    response = json.loads(response.text)
    return response['token']


class HiveControls:

    def __init__(self):
        self.token = get_access_token()
        print(self.token)

    def run_action(self, uid):
        url = "http://beekeeper-uk.hivehome.com/1.0/actions/%s/quick-action"
        url = url % uid

        payload = ""
        headers = {
            'content-type': "application/json",
            'Authorization': "Bearer %s" % self.token,
            'cache-control': "no-cache",
            'Postman-Token': "bea4fb4d-be78-4b87-bea3-666f23fd1df5"
        }

        response = requests.request("POST", url, data=payload,
                                    headers=headers, verify=False)

        print(response.text)

    def logout(self):
        url = "http://beekeeper-uk.hivehome.com/1.0/auth/logout"

        payload = ""
        headers = {
            'Accept': "*/*",
            'Origin': "https://my.hivehome.com",
            'Access-Control-Request-Method': "DELETE",
            'Access-Control-Request-Headers': "content-type, authorization",
            'Accept-Encoding': "gzip, deflate",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            'Host': "beekeeper-uk.hivehome.com",
            'Content-Length': "0",
            'Connection': "Keep-Alive",
            'Cache-Control': "no-cache",
            'cache-control': "no-cache",
            'Postman-Token': "55ac7403-68fc-460e-9099-8728ecee5970"
        }

        requests.request("OPTIONS", url, data=payload,
                         headers=headers, verify=False)

        payload = "{}"
        headers = {
            'Accept': "*/*",
            'content-type': "application/json",
            'Referer': "https://my.hivehome.com/text-control",
            'Accept-Language': "en-GB",
            'Origin': "https://my.hivehome.com",
            'Accept-Encoding': "gzip, deflate",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            'Host': "beekeeper-uk.hivehome.com",
            'Content-Length': "2",
            'Connection': "Keep-Alive",
            'Cache-Control': "no-cache",
            'Authorization': "Bearer %s" % self.token,
            'cache-control': "no-cache",
            'Postman-Token': "94e2dd8b-2619-4909-a666-c491a0a18a29"
        }

        requests.request("DELETE", url, data=payload,
                         headers=headers, verify=False)

    def get_token(self):
        return self.token

    # def __del__(self):
    #     logout()


if __name__ == "__main__":
    hive = HiveControls()
    hive.run_action('54c65147-2848-4b50-bc56-32e62ed96777')
    hive.logout()
