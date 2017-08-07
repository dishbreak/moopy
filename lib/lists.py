import common
from xml.etree import ElementTree
import sys


def get_lists():
    params = {}
    params['method'] = 'rtm.lists.getList'

    result = common.perform_request(params)

    return [tag.attrib for tag in result]


def get_list_by_name(name=None):
    list_of_lists = get_lists()
    if name is None:
        return list_of_lists[0]
    else:
        for list_iter in list_of_lists:
            if list_iter['name'] == name:
                list_obj = list_iter
                break
        if list_iter is None:
            print("Whoops! No list named '{}'".format(args[0]))
            sys.exit(1)

        return list_iter
