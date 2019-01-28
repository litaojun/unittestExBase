#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 
http://blog.csdn.net/jasonwoolf/article/details/47979655
@author: li.taojun
'''
import unittest
from opg.util.lginfo import  logger
class ParametrizedTestCase(unittest.case.TestCase):
    """
        TestCase classes that want to be parametrized should
        inherit from this class.
    """
    def __init__(self, methodName='runTest', param=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.param = param
        self.myservice  = None
        self.inputdata = self.getInputData()
        self.expectdata = self.getExpectData()
        logger.info(msg="类=%s,接口=%s,用例ID=%s执行开始"%(self.__class__,
                                                             self.__class__.__interfaceName__,
                                                             self.getCaseid()))
    def setService(self,myservice):
        self.myservice = myservice
        self.myservice.initInterfaceData()
        
    def setUp(self):
        predata = self.getPreConditions()
        if predata is not None:
           dbsqlls = [sql for sql in predata if  sql.startswith("preDB")]
           for pre in predata:
               if pre.startswith("setup"):
                  if pre in self.myservice.ifacedict:
                     preReqJsonFile  = self.myservice.ifacedict[pre][0]
                     if  preReqJsonFile is not None:
                         inputFormat = self.myservice.inputKV["reqjsonfile"]
                         self.myservice.inputKV["reqjsonfile"] = self.myservice.inputKV[preReqJsonFile]
                     self.myservice.ifacedict[pre][1]()
                     if  preReqJsonFile is not None:
                         self.myservice.inputKV["reqjsonfile"] = inputFormat

    def tearDown(self):
        predata = self.getPreConditions()
        if predata is not None:
              # dbsqlls = [ sql   for sql in predata if  sql.startswith("tearDB") ]
              # self.myservice.handlingDb(dbsqlls)
              for pre in predata:
                  if pre.startswith("tearDown"):
                     if pre in self.myservice.ifacedict:
                        preReqJsonFile = self.myservice.ifacedict[pre][0]
                        if preReqJsonFile is not None:
                           inputFormat = self.myservice.inputKV["reqjsonfile"]
                           self.myservice.inputKV["reqjsonfile"] = self.myservice.inputKV[preReqJsonFile]
                        self.myservice.ifacedict[pre][1]()
                        if preReqJsonFile is not None:
                           self.myservice.inputKV["reqjsonfile"] = inputFormat
                  if pre.startswith("tearDB"):
                     self.myservice.handlingOneDb(pre)
        logger.info(msg="类=%s,接口=%s,用例ID=%s执行结束" % (self.__class__, self.__class__.__interfaceName__, self.getCaseid()))

    def setCleanData(self,cleandata):
        self.cleandata = cleandata

    def getInputData(self):
        return self.param[5]

    def getCaseid(self):
        return self.param[0]

    def getTestPoint(self):
        return self.param[2]

    def getExpectData(self):
        return self.param[6]

    def getPreConditions(self):
        return self.param[3]

    @staticmethod
    #===========================================================================
    # parametrize
    #根据测试类（继承了ParametrizedTestCase）和测试数据（从excel读取）构成TestCase
    #===========================================================================
    def parametrize(testcase_klass, params={}):
        """
            Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        suite = unittest.TestSuite()
        testnames = params.keys()
        for name in testnames:
            casels = params[name]
            for onecase in casels:
                 if hasattr(testcase_klass, name):
                    suite.addTest(testcase_klass( name , onecase ))
                 else:
                    print("%s类不存在%s方法" % (testcase_klass.__name__,name))
        return suite

    def compareRetcodeTest(self):
        self.rsp  = self.myservice.sendHttpReq()
        retcode   = self.myservice.getRetcodeByRsp(response = self.rsp)
        self.assertTrue(retcode == self.expectdata["code"],
                         msg    = "expect code is %s,actual code is %s" % (self.expectdata["code"],retcode))
        compareDataList = self.expectdata.get("compare",[])
        for compareData in compareDataList:
            testPoint  = compareData["comparePoint"]
            expectData = compareData["expectData"]
            cprFun     = getattr(self,compareData["fun"])
            sign       = compareData.get("sign",True)
            if sign:
               expectFunData = self.myservice.compareFuncDict.get(expectData,expectData)
               expectData    = expectFunData() if (hasattr(expectFunData, '__call__')) else expectFunData
               actualData    = self.myservice.compareFuncDict.get(compareData["actualData"])()
               cprFun(expectData,actualData,"testPoint is %s,expectData is %s,actualData is %s" %
                                             (testPoint,str(expectData),str(actualData)))

    def assertObject(self,expectData = None,actualData = None,compareFun = None,testPoint = None):
        funDict = {
                     "int"  : self.assertEqual ,
                     "str"  : self.assertEqual ,
                     "list" : self.assertListEqual,
                     "dict" : self.assertDictEqual
                   }
        compareFun = funDict[typeof(actualData)] if compareFun is None else compareFun
        compareFun(expectData,actualData,"testPoint is %s,expectData is %s,actualData is %s" %
                           (testPoint,str(expectData),str(actualData)))







    def id(self):
        return "%s.%s_%s" % (self.__class__.__interfaceName__ + "--" + self.param[0], self.param[0], self.param[2])
# 判断变量类型的函数
def typeof(variate):
    type = None
    if isinstance(variate, int):
       type = "int"
    elif isinstance(variate, str):
         type = "str"
    elif isinstance(variate, float):
         type = "float"
    elif isinstance(variate, list):
         type = "list"
    elif isinstance(variate, tuple):
         type = "tuple"
    elif isinstance(variate, dict):
         type = "dict"
    elif isinstance(variate, set):
         type = "set"
    return type
#####################################################
##-testcase
#####################################################
class TestOneZgr(ParametrizedTestCase):
    __interfaceName__ = "baomingzgr"

    def test_something(self):
        self.assertEqual(1, 1)

    def test_something_else(self):
        self.assertEqual(2, 2)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTestCase.parametrize(TestOneZgr, params={"test_something":[6,22,33]}))
    suite.addTest(ParametrizedTestCase.parametrize(TestOneZgr, params={"test_something_else":[6,22,33]}))
    unittest.TextTestRunner(verbosity=2).run(suite)