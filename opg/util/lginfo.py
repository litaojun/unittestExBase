#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: Lieb 
@license: Apache Licence  
@contact: 2750416737@qq.com 
@site: http://blog.csdn.net/hqzxsc2006 
@software: PyCharm 
@file: lginfo.py 
@time: 2018/6/11 15:33 
"""
import logging  # 引入logging模块
import os.path,os
import time
#from steam.util.reqFormatPath  import  fxt
#from opg.unit.parametrized import ParametrizedTestCase
# from steam.user.login.userLoginService import WeixinUserLoginService
# from steam.user.verfiycode.userVerfiyCodeService import WeixinUserVerfiyCodeService
# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关

# 第二步，创建一个handler，用于写入日志文件
# rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
# #log_path = os.path.dirname(os.getcwd()) + fxt + 'Logs' + fxt
# log_path = os.getcwd() + os.sep + 'Logs' + os.sep
# log_name = log_path + rq + '.log'
# logfile = log_name
# #handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8')  # 实例化handler
# fh = logging.FileHandler(logfile, mode='w',encoding="utf-8")
# fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
# # 第三步，定义handler的输出格式
# formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
# fh.setFormatter(formatter)
# # 第四步，将logger添加到handler里面
# logger.addHandler(fh)
# logger.addHandler(handler)
# 日志
# logger.debug('this is a logger debug message')
# logger.info('this is a logger info message')
# logger.warning('this is a logger warning message')
# logger.error('this is a logger error message')
# logger.critical('this is a logger critical message')
def genDir():
    rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    log_path = os.getcwd() + os.sep + 'Logs' + os.sep
    log_name = log_path + rq
    logDir = log_name
    os.mkdir(logDir)
    return logDir
# logDir = genDir()

def writeLog(wtrDir=None):
    ifsDict = {}
    def createLogFile(interfaceSign = None,className=None,caseId=None):
        """
        :param interfaceSign:  None:创建目录，否则创建日志文件
        :return:
        """
        # if logger.hasHandlers():
        #     for curHandle in logger.handlers:
        #         logger.removeHandler(curHandle)
        # log_path = os.getcwd() + os.sep + 'Logs' + os.sep + wtrDir + os.sep
        logfile = wtrDir + os.sep + interfaceSign.replace("/","-")[1:-1]  + '.log'
        if interfaceSign not in ifsDict:
           fh = logging.FileHandler(logfile, mode='w',encoding="utf-8")
           ifsDict[interfaceSign] =  fh
           fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
           # 第三步，定义handler的输出格式
           formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
           fh.setFormatter(formatter)
        else:
           fh=ifsDict[interfaceSign]
        # 第四步，将logger添加到handler里面
        # logger.addHandler(fh)
        # logger.info(msg="类=%s,接口=%s,用例ID=%s执行开始"%(className,
        #                                                      interfaceSign,
        #                                                      caseId))
        return fh
    return createLogFile

def selectFh(fh=None,sign=True):
    """
    :param fh:  日志输出handle
    :param sign: True 增加handle;   False 移除handle;
    :return:
    """
    # if logger.hasHandlers():
    #     for curHandle in logger.handlers:
    #         logger.removeHandler(curHandle)
    if sign:
       logger.addHandler(fh)
    else:
        logger.removeHandler(fh)
writeDir = None
# writeDir = writeLog(wtrDir=logDir)

if __name__ == "__main__":
    def a(sign):
        t = {}
        def b(a,b):
            if a not in t:
                t[a] = (sign,b)
            else:
                print(t)
        return b
    f = a("aaa")
    f("fff","cccc")
    f("fff1", "cccc1")
    f("fff2", "cccc2")
    f("fff3", "cccc3")
    f("fff", "ccccff")