import json
import certifi
import urllib3

from secure.logons import hive_user, hive_password

HTTP = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where())
MAKE_REQ = HTTP.request


def get_sign_on():
    """
    Sign into Hive and return the json response containing the token and possible actions.
    """
    url = "https://beekeeper.hivehome.com/1.0/global/login"

    payload = "{\"username\": \"%s\", " \
              "\"password\": \"%s\", " \
              "\"devices\": true, " \
              "\"products\": true, " \
              "\"actions\": true, " \
              "\"homes\": true}" % (hive_user, hive_password)
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'Postman-Token': "1a8d9050-f7ae-4246-9afe-6dae9baddb2e"
    }

    response = MAKE_REQ("POST", url, body=payload,
                        headers=headers)  # , verify=False)
    response = response.data.decode('utf-8')
    return json.loads(response)


class HiveControls:
    def __init__(self):
        self.response = get_sign_on()
        self.token = self.response['token']

    def get_actions(self):
        """
        Parse the logon response for possible options
        """
        return self.response['actions']

    def get_devices(self):
        """
        Parse the logon response for available devices
        """
        return self.response['devices']

    def run_action_by_name(self, name):
        """
        Run a hive action by name. For example "Shed heater on". It does this by parsing the
        logon response for the action name and getting the associated uid which can be run by
        `run_action_by_uid`
        """
        name = name.lower()
        actions = self.get_actions()
        try:
            action = [x for x in actions if x['name'].lower() == name][0]
        except IndexError:
            raise IndexError("Action not found in list from Hive, do you have the right name? \n%s" % actions)
        uid = action['id']
        self.run_action_by_uid(uid)

    def run_action_by_uid(self, uid):
        """
        Run a hive action by uid string. Simply pings the quick action API and prints the response.
        """
        if uid is None:
            print("No associated Hive action")
            return

        url = "https://beekeeper-uk.hivehome.com/1.0/actions/%s/quick-action"
        url = url % uid

        payload = ""
        headers = {
            'content-type': "application/json",
            'Authorization': "Bearer %s" % self.token,
            'cache-control': "no-cache",
            'Postman-Token': "bea4fb4d-be78-4b87-bea3-666f23fd1df5"
        }

        resp = MAKE_REQ("POST", url, body=payload,
                        headers=headers)  # , verify=False)
        print('Action %s complete. Response: %s' %
              (uid, resp.data.decode('utf-8')))

    def logout(self):
        """
        Logout from Hive and thus invalidate your token.
        """
        url = "https://beekeeper-uk.hivehome.com/1.0/auth/logout"

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

        MAKE_REQ("OPTIONS", url, body=payload,
                 headers=headers)  # , verify=False)

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

        MAKE_REQ("DELETE", url, body=payload,
                 headers=headers)  # , verify=False)
        print("logged out")

    def get_token(self):
        return self.token


if __name__ == "__main__":
    hive = HiveControls()
    # hive.run_action_by_uid(actions['shed_heater_on'])
    hive.run_action_by_name('boost shed heater')
    print(hive.get_actions())
    print(hive.get_devices())
    hive.logout()
