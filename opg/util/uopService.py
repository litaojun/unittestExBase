#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年12月29日 上午11:34:48
@author: li.taojun
'''
import os
from opg.util.xmlParseTool  import Xml_Parserfile
from opg.util.dbtools import DbManager
from inspect import ismethod
# from opg.util.schemajson import loadStrFromFile
import time,functools
from opg.util.fileOper import walk_dir_test
from opg.util.lginfo import logger
def decorator(param):
    def _decorator(fun):
        if not isinstance(fun, type):
           @functools.wraps(fun)
           def wrapper(*args, **kwargs):
               logger.info(msg="前置调用函数%s,类%s" % (fun.__name__, str(args[0])))
               start   = time.time()
               rsp = fun(*args, **kwargs)
               runtime = time.time() - start
               return rsp
           wrapper.__decorator__ = True
           wrapper.__param__     = param
        return wrapper
    return _decorator

def resultData(param):
    def _resultData(fun):
        if not isinstance(fun, type):
           @functools.wraps(fun)
           def wrapper(*args, **kwargs):
               logger.info(msg="前置调用函数%s,类%s" % (fun.__name__, str(args[0])))
               start   = time.time()
               rsp = fun(*args, **kwargs)
               runtime = time.time() - start
               return rsp
           wrapper.__resultData__ = True
           wrapper.__param__     = param
        return wrapper
    return _resultData
def loadStrFromFile(filepath = ""):
    load_str = ""
    if os.path.exists(filepath):
        with open(filepath, 'r',encoding="utf-8") as load_f:
             lines    = load_f.readlines()
             load_str = "".join(lines)
             load_str = load_str.replace("\n\t", "")
    return load_str

class UopService(object):
    """

    """
    fmtdict = None
    token = None
    def __init__(self,module       = ""  ,
                      filename     = ""  ,
                      sqlvaluedict = {}  ,
                      reqjsonfile  = None ,
                      dbName       = "resource"):
        """
            :param module :
            :param filename :
            :param sqlvaluedict :
        """
        self.jsonheart = {
                            "x-token"  : "admin" ,
                            "memberId" : sqlvaluedict["memberId"] if "memberId" in sqlvaluedict else "" ,
                            "token"    :  sqlvaluedict["token"] if "token" in sqlvaluedict else ""
                          }
        self.module   = module
        self.filename = filename
        self.inputKV  = sqlvaluedict
        self.sqldict  = {}
        self.ifacedict   = {}
        self.compareFuncDict = {}
        self.reqjsondata = ""
        self.rsp         = None
        self.lsser       = [self,]
        self.dbManager   = DbManager(host  =  "steam-uat-default.crbcfaeazoqe.rds.cn-northwest-1.amazonaws.com.cn",
                                     user  =  "root",
                                     password = "Bestv001!",
                                     dbname   = dbName,
                                     port     = 3306)
        #self.initDbOperator()
        UopService.initFmtDict()
        self.initReqJsonData( reqjsonfile = reqjsonfile ,
                              reqjsondata = self.inputKV )

    @classmethod
    def initFmtDict(cls):
        if cls.fmtdict is None:
           cls.fmtdict = {}
           a = walk_dir_test( dir = os.getcwd() , sign = "Req" , endstr = ".txt" )
           b = walk_dir_test( dir = os.getcwd() , sign = "Fmt" , endstr = ".json")
           for cs in a + b:
               cls.fmtdict[os.path.basename(cs).split(".")[0]] = cs

    def resetToken(self):
        pass

    def initReqJsonData(self,reqjsonfile = "",reqjsondata = None):
        self.reqjsondata = self.getReqJsonData(reqjsonfile = reqjsonfile,
                                               reqjsondata = reqjsondata)

    def getReqJsonData(self,reqjsonfile = "",
                            reqjsondata = None):
        jsondata = None
        if reqjsonfile is not None and reqjsondata != "":
           if reqjsonfile.endswith(".txt"):
              jsonpath = os.getcwd() + reqjsonfile
           else:
              jsonpath = UopService.fmtdict[reqjsonfile]
           reqDataFmt   = loadStrFromFile(filepath = jsonpath)
           reqdata     = reqDataFmt % reqjsondata
           try:
              jsondata = eval(reqdata)
           except SyntaxError as err:
              jsondata = reqdata
              print("SyntaxError:",err)
           except Exception as e:
              raise e
           return jsondata

    def initInterfaceDict(self):
        for name in dir(self):
            funObj = getattr(self, name)
            if ismethod(funObj)  :
                curdoc = getattr(funObj , "__doc__")
                if curdoc is not None:
                    #print("curdoc"+str(curdoc))
                    sign = curdoc.split("\n")[1].strip()
                    if sign.startswith("Sign"):
                       funSign = sign.split(":")[1]
                       self.ifacedict[funSign] = funObj

    def initInterfaceData(self,sign = None):
        for name in dir(self):
            funObj = getattr(self, name)
            #if ismethod(funObj) and (sign or (name != "sendHttpReq")):
            if ismethod(funObj):
               signDec  = getattr(funObj, "__decorator__",False)
               signName = getattr(funObj, "__param__", False)
               if signDec :
                  if isinstance(signName,str):
                     self.ifacedict[signName] = [sign,funObj]
                  else:
                     if isinstance(signName,list):
                        for name in signName:
                            self.ifacedict[name] = [sign,funObj]

    def initCompareResultFunData(self,sign = None):
        for name in dir(self):
            funObj = getattr(self, name)
            #if ismethod(funObj) and (sign or (name != "sendHttpReq")):
            if ismethod(funObj):
               signDec  = getattr(funObj, "__resultData__",False)
               signName = getattr(funObj, "__param__", False)
               if signDec :
                  if isinstance(signName,str):
                     self.compareFuncDict[signName] = funObj
                  else:
                     if isinstance(signName,list):
                        for name in signName:
                            self.compareFuncDict[name] = funObj

    def initInterfaceDataT(self):
        for serv in self.lsser:
            for name in dir(serv):
                funObj = getattr(serv, name)
                if ismethod(funObj):
                    signDec = getattr(funObj, "__decorator__",False)
                    signName = getattr(funObj, "__param__", False)
                    if signDec :
                        if isinstance(signName,str):
                            self.ifacedict[signName] = funObj
                        else:
                            if isinstance(signName,list):
                               for name in signName:
                                   self.ifacedict[name] = funObj

    def initDbOperator(self):
        if self.filename is not None and self.filename != "" :
            xmlsqlpath = os.path.join(os.getcwd(),
                                      'steamdb',
                                      self.module, self.filename)
            xmlsqlfile = Xml_Parserfile(filename = xmlsqlpath)
            itsql = xmlsqlfile.parserSql()
            #a = self.inputKV
            for cursql in itsql :
                self.sqldict[cursql[0]] = (cursql[1],cursql[2] % self.inputKV,cursql[3])


    def getTownList(self,predata = []):
        """
            :param predata:
            :return:
        """
        prels = []
        if predata is not None:
            for pre in predata:
                prels.append(self.sqldict[pre][2])
        return prels

    def handlingDb(self,sqlls = ()):
        """
            :param sqlls:
            :return:
        """
        self.initDbOperator()
        operDict = {
                      "delete":self.dbManager.deleteData,
                      "add":self.dbManager.insertData,
                      "update":self.dbManager.updateData
                   }
        # f = lambda x:operDict[self.sqldict[x][0]](self.sqldict[x][1]) if x is not None else None
        # als = list(map(f,sqlls))
        for sqlSign in sqlls:
            sqlOperType = self.sqldict[sqlSign][0]
            sqlStr      = self.sqldict[sqlSign][1]
            operDict[sqlOperType](sqlStr)

    def handlingInterface(self , interacels = ()):
        f = lambda x:self.ifacedict[x][1]()
        rst = list(map(f,interacels))
        print(rst)

    def getDbManager(self):
        return self.dbManager

    def selectBySqlName(self,sqlname):
        sqlstr = self.sqldict[sqlname][1]
        qurResult = self.dbManager.queryAll(sqlstr)
        if qurResult is not None and len(qurResult)>0:
           return qurResult[0][0]
        return None

    def selectAllDataBySqlName(self,sqlname):
        sqlstr = self.sqldict[sqlname][1]
        qurResult = self.dbManager.queryAll(sqlstr)
        return qurResult

    def setInPutData(self):
        pass

    def sendInterfaceUrlReq(self):
        pass

    # def getRetcodeByRsp(response=None,
    #                     format="code"):
    #     pass

if __name__ == '__main__':
  pt  = os.path.abspath(os.path.join(os.getcwd(), "../.."))
  print(pt)
  t = {"a":"b","c":"d"}
  for m in t:
      print(m)