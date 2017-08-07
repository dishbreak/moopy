import common
from xml.etree import ElementTree


def get_lists():
    params = {}
    params['method'] = 'rtm.lists.getList'

    result = common.perform_request(params)

    return [tag.attrib for tag in result]
