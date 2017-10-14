""" GrSU API using
    """

import requests


def _grsuAPI_get_request(request_tail):
    """ HTTP GET request template for GrSU API """
    r = requests.get("http://api.grsu.by/1.x/app1/get{}".format(request_tail))
    return r.json()


def get_faculties_list():
    """ return list of faculty names
        and id's to use it in next requests """
    request_tail = "Faculties"
    data_json = _grsuAPI_get_request(request_tail)
    if "items" in data_json:
        return data_json["items"]
    else:
        raise Exception(str(data_json))


def get_groups_list(faculty_id, course):
    """ return list of faculty groups
        studying in defined course """
    request_tail = "Groups?departmentId={}&facultyId={}&course={}".format(2, faculty_id, course)
    data_json = _grsuAPI_get_request(request_tail)
    if "items" in data_json.keys():
        return data_json["items"]
    else:
        raise Exception(str(data_json))


def get_group_schedule(group_id, date_start, date_end):
    """ return list of dicts,
        where lessons grouped by date """
    request_tail = "GroupSchedule?groupId={}&dateStart={}&dateEnd={}".format(group_id, date_start, date_end)
    data_json = _grsuAPI_get_request(request_tail)
    if "days" in data_json.keys():
        return data_json["days"]
    else:
        raise Exception(str(data_json))

