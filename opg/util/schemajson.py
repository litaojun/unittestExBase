#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017

https://blog.csdn.net/a_finder/article/details/46746559
#http://json-schema.org/latest/json-schema-validation.html#anchor94
https://jsonschema.net/#/home
@author: li.taojun
'''
import json
#from jsonschema import validators 
#from jsonschema import validate
from jsonschema import Draft4Validator
from functools import wraps
from jsonschema import FormatChecker
from jsonschema import ValidationError
import os,sys
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
            #OG.exception(ex.message)
            # TODO(ramineni):raise valence specific exception
            print(ex.message)
            print("type="+str(type(ex)))
            print("dir="+str(dir(ex)))
            print("ex.message="+str(type(ex.message)))
            raise Exception(ex.message)

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
            # while line:
            #     line = line.strip('\n')
            #     load_str = load_str + line
            #     line = load_f.readline()
    return load_str


##validator.py
def check_rspdata(filepath):
    def decorated(f):
#         @wraps(f)
        def wrapper(*args, **kwargs):
            print ("kwargs="+str(kwargs))
            jsondata = kwargs["response"]
            #LOG.debug("validating input %s with %s", data, validator.name)
            file = os.getcwd() + filepath
            print("file=%s" % file)
            activitiesInfoScma = loadJsonFile(file)
            validator = Validator(activitiesInfoScma)
            #jsondata = {"code":"000000","message":"成功","data":None}
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