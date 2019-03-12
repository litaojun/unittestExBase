from requests.structures import CaseInsensitiveDict


def query_json(json_content, query, delimiter='.'):
    """ Do an xpath-like query with json_content.
    @param (json_content) json_content
        json_content = {
            "ids": [1, 2, 3, 4],
            "person": {
                "name": {
                    "first_name": "Leo",
                    "last_name": "Lee",
                },
                "age": 29,
                "cities": ["Guangzhou", "Shenzhen"]
            }
        }
    @param (str) query
        "person.name.first_name"  =>  "Leo"
        "person.cities.0"         =>  "Guangzhou"
    @return queried result
    """
    if json_content == "":
        raise Exception("response content is empty!")

    try:
        for key in query.split(delimiter):
            if isinstance(json_content, list):
                json_content = json_content[int(key)]
            elif isinstance(json_content, (dict, CaseInsensitiveDict)):
                json_content = json_content[key]
            else:
                raise Exception(
                    "response content is in text format! failed to query key {}!".format(key))
    except (KeyError, ValueError, IndexError):
        raise Exception("failed to query json when extracting response!")

    return json_content


def setValue_json(json_content, query, setvalue, delimiter='.'):
    """ Do an xpath-like query with json_content.
    @param (json_content) json_content
        json_content = {
            "ids": [1, 2, 3, 4],
            "person": {
                "name": {
                    "first_name": "Leo",
                    "last_name": "Lee",
                },
                "age": 29,
                "cities": ["Guangzhou", "Shenzhen"]
            }
        }
    @param (str) query
        "person.name.first_name"  =>  "Leo"
        "person.cities.0"         =>  "Guangzhou"
    @return queried result
    """
    if json_content == "":
        raise Exception("response content is empty!")
    sign = 0  # 0代表非列表
    lastkey = query
    json_content_pre = json_content
    try:
        for key in query.split(delimiter):
            lastkey = key
            json_content_pre = json_content
            if isinstance(json_content, list):
                json_content = json_content[int(key)]
                sign = 1
            elif isinstance(json_content, (dict, CaseInsensitiveDict)):
                json_content = json_content[key]
                sign = 0
            else:
                raise Exception(
                    "response content is in text format! failed to query key {}!".format(key))
    except (KeyError, ValueError, IndexError):
        raise Exception("failed to query json when extracting response!")
    if sign == 0:
        json_content_pre[lastkey] = setvalue
    else:
        json_content_pre[int(lastkey)] = setvalue

    # return json_content


def del_json_data(json_content, query, delimiter='.'):
    """ Do an xpath-like query with json_content.
    @param (json_content) json_content
        json_content = {
            "ids": [1, 2, 3, 4],
            "person": {
                "name": {
                    "first_name": "Leo",
                    "last_name": "Lee",
                },
                "age": 29,
                "cities": ["Guangzhou", "Shenzhen"]
            }
        }
    @param (str) query
        "person.name.first_name"  =>  "Leo"
        "person.cities.0"         =>  "Guangzhou"
    @return queried result
    """
    if json_content == "":
        raise Exception("response content is empty!")
    sign = 0  # 0代表非列表
    lastkey = query
    json_content_pre = json_content
    try:
        for key in query.split(delimiter):
            lastkey = key
            json_content_pre = json_content
            if isinstance(json_content, list):
                json_content = json_content[int(key)]
                sign = 1
            elif isinstance(json_content, (dict, CaseInsensitiveDict)):
                json_content = json_content[key]
                sign = 0
            else:
                raise Exception(
                    "response content is in text format! failed to query key {}!".format(key))
    except (KeyError, ValueError, IndexError):
        raise Exception("failed to query json when extracting response!")
    if sign == 0:
        del json_content_pre[lastkey]  # = setvalue
    else:
        del json_content_pre[int(lastkey)]  # = setvalue


if __name__ == "__main__":
    json_content = {
        "code": "000000",
        "ids": [1, 2, 3, 4],
        "person": {
            "name": {
                "first_name": "Leo",
                "last_name": "Lee",
            },
            "age": 29,
            "cities": ["Guangzhou", "Shenzhen"]
        }
    }
    a = query_json(json_content, "ids.1")
    print(a)
    code = query_json(json_content, "code")
    print(code)
    setValue_json(json_content, "ids.1", 9)
    print(str(json_content))
    setValue_json(json_content, "person.name.first_name", "testlitaojun")
    print(str(json_content))
    setValue_json(json_content, "code", "fffffs")
    del_json_data(json_content, "ids.1")
    print(json_content)
    del_json_data(json_content, "ids.2")
    print(json_content)
    del_json_data(json_content, "person.name.first_name")
    print(json_content)
    del_json_data(json_content, "person.cities.1")
    print(json_content)
    del_json_data(json_content, "person.cities.0")
    print(str(json_content))
