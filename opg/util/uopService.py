#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年12月29日 上午11:34:48
@author: li.taojun
'''
import os
from opg.util.xmlParseTool  import Xml_Parserfile
from opg.util.dbtools import DbManager
from inspect import isfunction,ismethod
import time,functools
def decorator(param):
    def _decorator(fun):
        if not isinstance(fun, type):
            @functools.wraps(fun)
            def wrapper(*args, **kwargs):
                start = time.time()
                fun(*args, **kwargs)
                runtime = time.time() - start
            wrapper.__decorator__ = True
            wrapper.__param__ = param
        return wrapper
    return _decorator

class UopService(object):
    """

    """
    def __init__(self,module,filename,sqlvaluedict):
        """
            :param module :
            :param filename :
            :param sqlvaluedict :
        """
        self.module = module
        self.filename = filename
        self.sqlvaluedict = sqlvaluedict
        self.sqldict = {}
        self.ifacedict = {}
        self.dbManager = DbManager(host="uop-dev-wx.cmcutmukkzyn.rds.cn-north-1.amazonaws.com.cn",
                                   user="root",
                                   password="Bestv001!",
                                   dbname="uop",
                                   port=3306)
        self.initDbOperator()
        # self.initInterfaceDict()

    def initInterfaceDict(self):
        for name in dir(self):
            funObj = getattr(self, name)
            if ismethod(funObj)  :
                curdoc = getattr(funObj, "__doc__")
                if curdoc is not None:
                    print("curdoc"+str(curdoc))
                    sign = curdoc.split("\n")[1].strip()
                    if sign.startswith("Sign"):
                       funSign = sign.split(":")[1]
                       print("funSign = %s" % funSign)
                       self.ifacedict[funSign] = funObj

    def initInterfaceData(self):
        for name in dir(self):
            funObj = getattr(self, name)
            if ismethod(funObj):
                signDec = getattr(funObj, "__decorator__",False)
                signName = getattr(funObj, "__param__", False)
                if signDec :
                    self.ifacedict[signName] = funObj

    def initDbOperator(self):
        if self.filename is not None and self.filename != "" :
            # cwdt = os.getcwd()
            # cwdps = os.path.join(os.getcwd())
            # xmlsqlpath = os.path.join(os.path.abspath(os.path.join(os.getcwd())), "uopdb", "weixin",
            #                           self.module, self.filename)
            xmlsqlpath = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "../../..")), "uopdb", "weixin",
                                      self.module, self.filename)
            xmlsqlfile = Xml_Parserfile(filename = xmlsqlpath)
            itsql = xmlsqlfile.parserSql()
            a = self.sqlvaluedict
            for cursql in itsql :
                self.sqldict[cursql[0]] = (cursql[1],cursql[2] % self.sqlvaluedict,cursql[3])

    # def getTownList(self,prels):
    #     townls = []
    #     for cursql in self.sqldict:
    #         if self.sqldict[cursql][3] is not None:
    #             townls.append(self.sqldict[cursql][3])
    #     return townls

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
        operDict = {
                      "delete":self.dbManager.deleteData,
                      "add":self.dbManager.insertData,
                      "update":self.dbManager.updateData
                   }
        f = lambda x:operDict[self.sqldict[x][0]](self.sqldict[x][1]) if x is not None else None
        als = list(map(f,sqlls))
        
    # def userSignupActivities(self):
    #     pass
    #
    # def userRemoveCollectionGoods(self):
    #     pass
    #
    # def userCollectionGoods(self):
    #     pass

    def handlingInterface(self,interacels = ()):
        f = lambda x:self.ifacedict[x]()
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
        
if __name__ == '__main__':
  pt  = os.path.abspath(os.path.join(os.getcwd(), "../.."))
  print(pt)
  t = {"a":"b","c":"d"}
  for m in t:
      print(m)