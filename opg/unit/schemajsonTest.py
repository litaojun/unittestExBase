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
from jsonschema import Draft4Validator
from jsonschema import FormatChecker
from jsonschema import ValidationError
class Validator(object):
    def __init__(self, schemaformat):
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
            #raise Exception(ex.message)


##validator.py
def check_rspdata(validator):
    def decorated(f):
#         @wraps(f)
        def wrapper(*args, **kwargs):
            print ("kwargs="+str(kwargs))
            jsondata = kwargs["response"]
            #LOG.debug("validating input %s with %s", data, validator.name)
            validator.validate(jsondata)
            return f(jsondata)
        return wrapper
    return decorated



schema = {
            "type" : "object",
            "properties" :
                        {
                            "price" : {"type" : "number"},
                            "name" :  {"type" : "string"},
                            "list":{"maxItems":1},
                            "address":{'regex':'bj'},
                        }
         }
schemast = {
             "type": "object",
             "properties": {
                                              "code": {
                                                        "type": "string",
                                                         "maxLength":5
                                                      },
                                              "message": {
                                                            "type": "string"
                                                          },
                                              "data": {
                                                        "type": "null"
                                                      }
                                            }
                            }
schemastt = {
  "$id": "addArticleRspFmt",
  "type": "object",
  "definitions": {},
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
                                      "code": {
                                                "$id": "/properties/code",
                                                "type": "string",
                                                "title": "The Code Schema ",
                                                # "maxLength":5,
                                                 "minLength":7,
                                                "default": ""
                                              },
                                      "message": {
                                                    "$id": "/properties/message",
                                                    "type": "string",
                                                    "title": "The Message Schema ",
                                                    "default": "",
                                                    "examples": [
                                                      "成功"
                                                    ]
                                                  },
                                      "data": {
                                                "$id": "/properties/data",
                                                "type": "null",
                                                "title": "The Data Schema ",
                                                "default": None,
                                                "examples": [
                                                    None
                                                ]
                                              }
                                    }
                    }
validator = Validator(schemastt)
@check_rspdata(validator)
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
    #jsonart = "{\"code\":\"000000\",\"message\":\"成功\",\"data\":None}"
    jsonart = {"code":"000000","message":"成功","data":None}
    a(response=jsonart)