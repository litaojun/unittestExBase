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
from opg.unit.parametrized import ParametrizedTestCase
# from steam.user.login.userLoginService import WeixinUserLoginService
# from steam.user.verfiycode.userVerfiyCodeService import WeixinUserVerfiyCodeService
# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
#log_path = os.path.dirname(os.getcwd()) + fxt + 'Logs' + fxt
log_path = os.getcwd() + os.sep + 'Logs' + os.sep
log_name = log_path + rq + '.log'
logfile = log_name
#handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8')  # 实例化handler
fh = logging.FileHandler(logfile, mode='w',encoding="utf-8")
fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
# 第四步，将logger添加到handler里面
logger.addHandler(fh)
#logger.addHandler(handler)
# 日志
# logger.debug('this is a logger debug message')
# logger.info('this is a logger info message')
# logger.warning('this is a logger warning message')
# logger.error('this is a logger error message')
# logger.critical('this is a logger critical message')