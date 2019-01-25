import requests
from opg.util.lginfo import logger
def httpGet(url = "" , headers = {}):
    logger.info("http request type:GET")
    logger.info("http request url:%s" % url)
    httpRsp = requests.get(url=url,
                           headers=headers,
                           verify=False)
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

def httpPutGet(url ="" ,headers = {}):
    logger.info("http request type:GET")
    logger.info("http request url:%s" % url)
    httpRsp = requests.put(
                                 url=url,
                                 headers=headers,
                                 verify=False
                              )
    logger.info("http response data:%s" % httpRsp.text)
    return httpRsp.text

def httpPostFile(url="",headers = {},file = None):
    logger.info("http request type:POST")
    logger.info("http request url:%s" % url)
    httpRsp = requests.post(
                                url=url,
                                files = file,
                                headers=headers,
                                verify=False
                            )
    logger.info("http response data:%s" % httpRsp.text)
    return httpRsp.text




