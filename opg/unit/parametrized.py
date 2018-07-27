#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 
http://blog.csdn.net/jasonwoolf/article/details/47979655
@author: li.taojun
'''
import logging,os
import unittest
from opg.util.lginfo import  logger
# from uopweixin.register.userRegService import UserRegisterService
class ParametrizedTestCase(unittest.case.TestCase):
    """
        TestCase classes that want to be parametrized should
        inherit from this class.
    """
    def __init__(self, methodName='runTest', param=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.param = param
        self.myservice = None
        self.inputdata = self.getInputData()
        self.expectdata = self.getExpectData()
        logger.info(msg="类=%s,接口=%s,用例ID=%s执行开始"%(self.__class__,self.__class__.__interfaceName__,self.getCaseid()))
        
    def setService(self,myservice):
        self.myservice = myservice
        self.myservice.initInterfaceData()
        print("litaojun")
        
    def setUp(self):
#           #后期抽奖前的个人总积分
#           self.preuserTotalPoint = self.personalCenterService.getPersonalSign()
          predata = self.getPreConditions()
          if predata is not None:
              dbsqlls = [sql for sql in predata if  sql.startswith("preDB")]
              interfacels = [infacename for infacename in predata if infacename.startswith("preInterface")]
              self.myservice.handlingDb(dbsqlls)
              self.myservice.handlingInterface(interfacels)
              
    def tearDown(self):
        predata = self.getPreConditions()
        if predata is not None:
              dbsqlls = [sql for sql in predata if  sql.startswith("tearDB")]
              interfacels = [infacename for infacename in predata if infacename.startswith("tearInterface")]
              self.myservice.handlingDb(dbsqlls)
              self.myservice.handlingInterface(interfacels)
        logger.info(msg="类=%s,接口=%s,用例ID=%s执行结束" % (self.__class__, self.__class__.__interfaceName__, self.getCaseid()))

    def setCleanData(self,cleandata):
        self.cleandata = cleandata

    def getInputData(self):
        jsonstr = "{"+ ",".join(self.param[5].split("\n")) + "}"
        dicdata = None
        try:
           dicdata =  eval(jsonstr)
        except Exception as ex:
            print(ex)
            print(jsonstr)
        return dicdata
    
    def getCaseid(self):
        return self.param[0]
    
    def getTestPoint(self):
        return self.param[2]
    
    def getExpectData(self):
        data = self.param[6]
        itemdata = data.split("\n")
        jsonstr = "{" + ",".join(itemdata) + "}"
        dicdata = eval(jsonstr)
        return dicdata

    def getPreConditions(self):
        itemdata = None
        data = self.param[3]
        if data is not None and data != "":
           itemdata = data.split("\n")
        return itemdata

    @staticmethod
    #===========================================================================
    # parametrize
    #根据测试类（继承了ParametrizedTestCase）和测试数据（从excel读取）构成TestCase
    #===========================================================================
    def parametrize(testcase_klass, params={}):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        suite = unittest.TestSuite()
        testnames = params.keys()
        for name in testnames:
            casels = params[name]
            for onecase in casels:
                 if hasattr(testcase_klass, name):
                     suite.addTest(testcase_klass(name,onecase))
                 else:
                     print("%s类不存在%s方法" % (testcase_klass.__name__,name))
        return suite

    def id(self):
        return "%s.%s_%s" % (self.__class__.__interfaceName__+"--"+self.param[0],self.param[0],self.param[2])

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