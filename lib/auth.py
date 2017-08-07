import requests
import hashlib
import constants
from xml.etree import ElementTree
import webbrowser
import os
import json

RTM_AUTH_SERVICE = "https://www.rememberthemilk.com/services/auth/"


def get_signature(params, shared_secret):
    keys = params.keys()
    keys.sort()
    md5 = hashlib.md5()

    md5.update(shared_secret)
    for key in keys:
        md5.update(key)
        md5.update(params[key])

    return md5.hexdigest()


def perform_request(params, shared_secret, url=constants.RTM_REST_URL):
    signature = get_signature(params, shared_secret)
    params['api_sig'] = signature
    return requests.get(constants.RTM_REST_URL, params=params)


def get_frob(api_key, shared_secret):
    params = {"api_key": api_key, "method": "rtm.auth.getFrob"}
    response = perform_request(params, shared_secret, RTM_AUTH_SERVICE)
    tree = ElementTree.fromstring(response.content)
    return tree[0].text


def process_token_response(xml_string):
    tree = ElementTree.fromstring(xml_string)
    token = tree[0].find('token').text

    moopy_path = os.path.expanduser('~/.moopy/')
    if not os.path.exists(moopy_path):
        os.mkdir(moopy_path)
    elif os.path.isfile(moopy_path):
        print("ERROR. There seems to be a file at {}.".format(moopy_path))
        print("Delete this file (or rename it) and try again.")

    f = open(moopy_path + "credentials", "w")
    f.write(token)
    f.close()

    return token


def get_token_from_rtm(api_key, shared_secret):
    frob = get_frob(api_key, shared_secret)
    params = {"api_key": api_key, "frob": frob, "perms": "delete"}
    signature = get_signature(params, shared_secret)
    params['api_sig'] = signature

    query_parts = []
    for key, value in params.iteritems():
        query_parts.append("{}={}".format(key, value))

    query_string = "&".join(query_parts)
    auth_url = "{}?{}".format(RTM_AUTH_SERVICE, query_string)

    print("Redirecting you to {}".format(auth_url))
    webbrowser.open_new(auth_url)

    raw_input("Press enter once you've authorized moopy.")
    params = {"api_key": api_key, "frob": frob, "method": "rtm.auth.getToken"}
    response = perform_request(params, shared_secret)

    token = process_token_response(response.text)
    return token


def is_authenticated():
    moopy_path = os.path.expanduser("~/.moopy/credentials")
    return os.path.exists(moopy_path)


def get_token():
    if not is_authenticated():
        print('Credentials not found, initating API authentication.')
        return get_token_from_rtm(constants.API_KEY, constants.SHARED_SECRET)
    else:
        f = open(os.path.expanduser('~/.moopy/credentials'), "r")
        token = f.read()
        f.close()
        return token