#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: Lieb 
@license: Apache Licence  
@contact: 2750416737@qq.com 
@site: http://blog.csdn.net/hqzxsc2006 
@software: PyCharm 
@file: httptools.py 
@time: 2018/6/11 16:48 
"""
import requests,json
from opg.util.utils import query_json
from opg.util.schemajson import check_rspdata
from opg.util.lginfo import  logger
def httpGet(url ="" ,headers = {}):
    logger.info("http request type:GET")
    logger.info("http request url:%s" % url)
    httpRsp = requests.get(
                                 url=url,
                                 headers=headers,
                                 verify=False
                            )
    logger.info("http response data:%s" % httpRsp.text)
    return httpRsp.text

def httpPost(url="",headers = {},reqJsonData = {}):
    logger.info("http request type:POST")
    logger.info("http request url:%s" % url)
    logger.info("http request data:%s" % reqJsonData)
    httpRsp = requests.post(
                                url=url,
                                json=reqJsonData,
                                headers=headers,
                                verify=False
                            )
    logger.info("http response data:%s" % httpRsp.text)
    return httpRsp.text

def httpDelete(url ="" ,headers = {}):
    logger.info("http request type:GET")
    logger.info("http request url:%s" % url)
    httpRsp = requests.delete(
                                 url=url,
                                 headers=headers,
                                 verify=False
                              )
    logger.info("http response data:%s" % httpRsp.text)
    return httpRsp.text




