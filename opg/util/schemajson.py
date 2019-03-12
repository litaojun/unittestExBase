import json
from opg.bak.uopService import UopService
#from jsonschema import validators 
#from jsonschema import validate
from jsonschema import Draft4Validator
from jsonschema import FormatChecker
from jsonschema import ValidationError
import os
from opg.util.lginfo import logger
class Validator(object):
    def __init__(self, schemaformat):
        #self.name = name
        self.schema = schemaformat
        checker = FormatChecker()
        self.validator = Draft4Validator(self.schema,
                                         format_checker=checker)

    def validate(self, data):
        try:
            self.validator.validate(data)
        except ValidationError as ex:
            # TODO(ramineni):raise valence specific exception
            print(ex.message)
            logger.error(ex)
            raise Exception(ex.message)
        except Exception as ex:
            logger.error(ex.message)
            raise Exception(ex.message)
        finally:
            print("vaild end")


def loadJsonFile(filepath = ""):
    load_dict = None
    if os.path.exists(filepath):
        with open(filepath, 'r',encoding='UTF-8') as load_f:
            load_dict = json.load(load_f)
    else:
        print("文件%s不存在" % filepath)
    return load_dict


def loadStrFromFile(filepath = ""):
    load_str = ""
    if os.path.exists(filepath):
        with open(filepath, 'r') as load_f:
            lines = load_f.readlines()
            load_str = "".join(lines)
            load_str = load_str.replace("\n\t", "")
    return load_str

def check_rspdata(filepath):
    def decorated(f):
#         @wraps(f)
        def wrapper(*args, **kwargs):
            jsondata = kwargs["response"]
            #LOG.debug("validating input %s with %s", data, validator.name)
            if filepath.endswith(".json"):
                 file = os.getcwd() + filepath
            else:
                file = UopService.fmtdict[filepath]
            activitiesInfoScma = loadJsonFile(file)
            validator = Validator(activitiesInfoScma)
            validator.validate(json.loads(jsondata))
            return f(*args,jsondata)
        return wrapper
    return decorated



schema = {
            "type" : "object",
            "properties" : 
                        {
                            "price" : {"type" : "number"},
                            "name" :  {"type" : "string"},
                            "list":{"maxItems":2},
                            "address":{'regex':'bj'},
                        }
         }
#validator = Validator(schema)
@check_rspdata("")
def a(response = None):
    #jsond = {"name" : "Eggs", "price" : 34.99,'list':[1,5,7],'address':'bj-jiuxianqiao'}
    #print "litaojun00000"
    return "litaojun"
if __name__ == '__main__':
    jsond = {
                  "name":"Eggs",
                  "price":34,
                  "list":[1,5],
                  "address":"bj-jiuxianqiao"
             }
    myjson = {"code":"000000","message":"成功","data":None}
    a(response=myjson)