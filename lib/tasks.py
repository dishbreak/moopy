import common


def get_list(list_id, filter=None):
    params = {}
    params['method'] = 'rtm.tasks.getList'

    if filter is not None:
        params['filter'] = filter
    params['list_id'] = list_id

    result = common.perform_request(params)

    task_list = [] if len(list(result)) == 0 else [
        tag.attrib for tag in result[0]]

    return task_list
