import auth
import constants
import requests
from xml.etree import ElementTree


def perform_request(params, is_authenticated=True, url=constants.RTM_REST_URL):
    if is_authenticated:
        params['auth_token'] = auth.get_token()

    params['api_key'] = constants.API_KEY
    params['api_sig'] = auth.get_signature(params)

    response = requests.get(url, params=params)
    # print("Response:")
    # print(response.text)

    return ElementTree.fromstring(response.text)[0]


def generate_timeline():
    response = perform_request(params={"method": "rtm.timelines.create"})
    return response.text
