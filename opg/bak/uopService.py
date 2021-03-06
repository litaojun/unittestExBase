import os
from opg.util.xmlParseTool  import Xml_Parserfile
from inspect import ismethod
import time,functools
from opg.util.fileOper import walk_dir_test
from opg.util.lginfo import logger
def decorator(param,userType = None):
    def _decorator(fun):
        if not isinstance(fun, type):
           @functools.wraps(fun)
           def wrapper(*args, **kwargs):
               logger.info(msg="前置调用函数%s,类%s" % (fun.__name__, str(args[0])))
               start   = time.time()
               if userType is not None:
                  args[0].inputKV["userType"] = userType
               rsp = fun(*args, **kwargs)
               if userType is not None:
                  del args[0].inputKV["userType"]
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
from opg.util.dbtools import Database
class UopService(object):
    fmtdict = None
    token = None
    def __init__(self,module       = ""  ,
                      filename     = ""  ,
                      sqlvaluedict = {}  ,
                      reqjsonfile  = None ,
                      dbName       = None):
        """
            :param module :
            :param filename :
            :param sqlvaluedict :
        """
        self.module   = module
        self.filename = filename
        self.inputKV  = sqlvaluedict
        self.sqldict  = {}
        self.ifacedict       = {}
        self.compareFuncDict = {}
        self.reqjsondata = ""
        self.rsp         = None
        self.lsser       = [self,]
        self.dbName      = dbName
        self.initDbOperator()
        UopService.initFmtDict()
        self.initReqJsonData( reqjsonfile = reqjsonfile ,
                              reqjsondata = self.inputKV )
        self.dbManager = Database()

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
            if ismethod(funObj):
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
               self.sqldict[cursql[0]] = (cursql[1], cursql[2] , cursql[3])

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
        if self.dbName is not None:
           # self.initDbOperator()
           # dbManager = Database()
           operDict = {
                         "delete" : self.dbManager.deleteData,
                         "add":      self.dbManager.insertData,
                         "update":  self.dbManager.updateData
                      }
           for sqlSign in sqlls:
               sqlOperType = self.sqldict[sqlSign][0]
               sqlStr      = self.sqldict[sqlSign][1] % self.inputKV
               operDict[sqlOperType](sqlStr,self.dbName)

    def handlingOneDb(self,sqlstr = ""):
        """
            :param sqlls:
            :return:
        """
        if self.dbName is not None:
           # self.initDbOperator()
           # dbManager = Database()
           operDict = {
                         "delete" : self.dbManager.deleteData,
                         "add":      self.dbManager.insertData,
                         "update":  self.dbManager.updateData
                      }
           sqlOperType = self.sqldict[sqlstr][0]
           sqlStr      = self.sqldict[sqlstr][1] % self.inputKV
           operDict[sqlOperType](sqlStr,self.dbName)

    def handlingInterface(self , interacels = ()):
        f = lambda x:self.ifacedict[x][1]()
        rst = list(map(f,interacels))
        print(rst)

    def getDbManager(self):
        return self.dbManager

    def selectBySqlName(self,sqlname):
        sqlstr    = self.sqldict[sqlname][1] % self.inputKV
        qurResult = self.dbManager.queryAll(sqlstr)
        if qurResult is not None and len(qurResult)>0:
           return qurResult[0][0]
        return None

    def selectAllDataBySqlName(self,sqlname):
        sqlstr = self.sqldict[sqlname][1] % self.inputKV
        qurResult = self.dbManager.queryAll(sqlstr,self.dbName)
        return qurResult

    def deleteBySqlName(self,sqlname):
        sqlstr = self.sqldict[sqlname][1] % self.inputKV
        self.dbManager.deleteData(sql = sqlstr,dbName=self.dbName)

    def setInPutData(self):
        pass

    def sendInterfaceUrlReq(self):
        pass

if __name__ == '__main__':
  pt  = os.path.abspath(os.path.join(os.getcwd(), "../.."))
  print(pt)
  t = {"a":"b","c":"d"}
  for m in t:
      print(m)