import logging  # 引入logging模块
import os.path
import os
import time

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


def genDir(logtime):
    logdir = os.sep.join([os.getcwd(),'Logs',logtime])
    if not os.path.exists(logdir):
       os.mkdir(logdir)
    return logdir

def writeLog(wtrDir=None,logtag="testcase"):
    ifsDict = {}
    #用例日志文件
    def createTscsLogFile(interfaceSign=None):
        """
        :param interfaceSign:  None:创建目录，否则创建日志文件
        :return:
        """
        logfile = wtrDir + os.sep + \
            interfaceSign.replace("/", "-")[1:] + '.log'
        if interfaceSign not in ifsDict:
            fh = logging.FileHandler(logfile, mode='w', encoding="utf-8")
            ifsDict[interfaceSign] = fh
            fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
            # 第三步，定义handler的输出格式
            formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
            fh.setFormatter(formatter)
        else:
            fh = ifsDict[interfaceSign]
        return fh
    def creatTokenLogFile():
        logfile = wtrDir + os.sep + "token.log"
        fh = logging.FileHandler(logfile, mode='w', encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        ifsDict["tokenlog"] = fh
        return fh
    if logtag == "testcase":
       return createTscsLogFile
    elif logtag == "tokenlog":
       return creatTokenLogFile



def selectFh(fh=None, sign=True):
    """
    :param fh:  日志输出handle
    :param sign: True 增加handle;   False 移除handle;
    :return:
    """
    if sign:
        logger.addHandler(fh)
    else:
        logger.removeHandler(fh)


writeDir = None

if __name__ == "__main__":
    def a(sign):
        t = {}

        def b(a, b):
            if a not in t:
                t[a] = (sign, b)
            else:
                print(t)
        return b
    f = a("aaa")
    f("fff", "cccc")
    f("fff1", "cccc1")
    f("fff2", "cccc2")
    f("fff3", "cccc3")
    f("fff", "ccccff")
