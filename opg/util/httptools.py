import requests
import json
import os
from opg.util.lginfo import logger

def httpReqSend(url="", headers={}, reqJson={},fileName="a.jpg",method="POST"):
    rsp = {}
    if method in ("get", "delete",  "put-get"):
        reqjsondata = "&".join([ "%s=%s" % (k,v) for k,v in reqJson.items() if v is not None])
        url+=reqjsondata
        if method == "get":
            rsp = httpGet(url=url,headers= headers)
        elif method == "delete":
            rsp = httpDelete(url=url,headers=headers)
        elif method == "file":
            filepath = os.getcwd() + os.path.sep + "steamcase" + os.path.sep + "%s"
            files = {'file': open(fileName, 'rb')}
            rsp = httpPostFile(url=url, headers=headers, file=files)
        elif method == "put-get":
            rsp = httpPutGet(url=url + reqjsondata,headers=headers)
    else:
        try:
            # if type(reqdata) == str:
            #     self.reqjsondata = eval(reqdata)
            if method == "post":
                rsp = httpPost(url=url,headers=headers,reqJsonData=reqJson)
            elif method == "put":
                rsp = httpDelete(url=url)
        except Exception as e:
            raise e
    return rsp

def jsonFmtPrint(jsondata=None):
    jsdt = None
    try:
        if isinstance(jsondata, str):
            jsdt = json.loads(jsondata, encoding="utf-8")
        elif isinstance(jsondata, dict):
            jsdt = jsondata
    except Exception as e:
        print(e)
        jsdt = jsondata
    finally:
        if isinstance(jsdt, dict):
            jstr = json.dumps(jsdt, indent=3, ensure_ascii=False)
            return jstr
        elif isinstance(jsdt, str):
            return jsdt

def httpGet(url="", headers={}):
    logger.info("http request type:GET")
    logger.info("http request url:%s" % url)
    logger.info("http request headers:%s" % jsonFmtPrint(jsondata=headers))
    httpRsp = requests.get(url=url,
                           headers=headers,
                           verify=False)
    a = "{'a':'测试'}"
    logger.info("测试http response data:%s" % jsonFmtPrint(a))
    print("李涛军---" + httpRsp.text)
    logger.info("测试http response data:%s" % jsonFmtPrint(httpRsp.text))
    return httpRsp.text


def httpPost(url="", headers={}, reqJsonData={}):
    logger.info("http request type:POST")
    logger.info("http request url:%s" % url)
    logger.info("http request headers:%s" % jsonFmtPrint(jsondata=headers))
    logger.info("http request data:%s" % jsonFmtPrint(reqJsonData))
    httpRsp = requests.post(
        url=url,
        json=reqJsonData,
        headers=headers,
        verify=False
    )
    logger.info("http response data:%s" % jsonFmtPrint(httpRsp.text))
    return httpRsp.text


def httpDelete(url="", headers={}):
    logger.info("http request type:GET")
    logger.info("http request url:%s" % url)
    logger.info("http request headers:%s" % jsonFmtPrint(jsondata=headers))
    httpRsp = requests.delete(
        url=url,
        headers=headers,
        verify=False
    )
    logger.info("http response data:%s" % jsonFmtPrint(httpRsp.text))
    return httpRsp.text


def httpPutGet(url="", headers={}):
    logger.info("http request type:GET")
    logger.info("http request url:%s" % url)
    logger.info("http request headers:%s" % jsonFmtPrint(jsondata=headers))
    httpRsp = requests.put(
        url=url,
        headers=headers,
        verify=False
    )
    logger.info("http response data:%s" % jsonFmtPrint(httpRsp.text))
    return httpRsp.text


def httpPostFile(url="", headers={}, file=None):
    logger.info("http request type:POST")
    logger.info("http request url:%s" % url)
    logger.info("http request headers:%s" % jsonFmtPrint(jsondata=headers))
    httpRsp = requests.post(
        url=url,
        files=file,
        headers=headers,
        verify=False
    )
    logger.info("http response data:%s" % jsonFmtPrint(httpRsp.text))
    return httpRsp.text
