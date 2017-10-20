import http.client
import json

try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+


class TSBackendConnector:
    __BASE_URL = None
    __OCP_APIM_SUBSCRIPTION_KEY = None
    __apiURL = None
    get_token = None

    def __init__(self, baseurl, get_token, ocp_apim_subscription_key, api_url):
        self.__BASE_URL = baseurl
        self.__apiURL = api_url
        self.get_token = get_token
        self.__OCP_APIM_SUBSCRIPTION_KEY = ocp_apim_subscription_key

    def base_headers(self):
        return {
            # Request headers
            'Authorization': 'Bearer ' + self.get_token(),
            'Ocp-Apim-Subscription-Key': self.__OCP_APIM_SUBSCRIPTION_KEY,
        }

    @staticmethod
    def add_json_to_header(header):
        header['Content-Type'] = 'application/json'

    def create_list(self, body):
        headers = self.base_headers()
        self.add_json_to_header(headers)

        conn = http.client.HTTPSConnection(self.__BASE_URL)
        conn.request("POST", "%s/api/v1/lists" % self.__apiURL, json.dumps(body), headers)
        response = conn.getresponse()
        data = response.read().decode('utf8')
        conn.close()
        return json.loads(data)

    def get_lists(self):
        headers = self.base_headers()

        conn = http.client.HTTPSConnection('kauflandstaging.azure-api.net')
        conn.request("GET", "%s/api/v1/lists" % self.__apiURL, "", headers)
        response = conn.getresponse()
        data = response.read().decode('utf8')
        conn.close()
        lists = json.loads(data)

        def id_lambda(x):
            x["id"] = x.get("_id")
            return x

        return map(id_lambda, lists)

    def add_list_elem(self, list_id, title, subtitle):
        headers = self.base_headers()
        self.add_json_to_header(headers)

        conn = http.client.HTTPSConnection('kauflandstaging.azure-api.net')
        conn.request("POST", "%s/api/v1/lists/%s/items" % (self.__apiURL, quote(list_id)),
                     json.dumps([{
                         'title': title,
                         'subtitle': subtitle
                     }]), headers)
        response = conn.getresponse()
        data = response.read().decode('utf8')
        print(data)
        return json.loads(data)
