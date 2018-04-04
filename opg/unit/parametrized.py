#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 
http://blog.csdn.net/jasonwoolf/article/details/47979655
@author: li.taojun
'''
import logging
import unittest
# from uopweixin.register.userRegService import UserRegisterService
class ParametrizedTestCase(unittest.case.TestCase):
    """
        TestCase classes that want to be parametrized should
        inherit from this class.
    """
    def __init__(self, methodName='runTest', param=None):
        logger = logging.getLogger("%s.%s" % (self.__class__.__name__, "__init__"))
        logger.setLevel(level=logging.INFO)
        handler = logging.FileHandler("log.txt")
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        super(ParametrizedTestCase, self).__init__(methodName)
        self.param = param
        self.myservice = None
        
    def setService(self,myservice):
        self.myservice = myservice
        self.myservice.initInterfaceData()
        
    def setUp(self):
#           #后期抽奖前的个人总积分
#           self.preuserTotalPoint = self.personalCenterService.getPersonalSign()
          predata = self.getPreConditions()
          if predata is not None:
              dbsqlls = [sql for sql in predata if not sql.startswith("interface")]
              interfacels = [infacename for infacename in predata if infacename.startswith("interface")]
              self.myservice.handlingDb(dbsqlls)
              self.myservice.handlingInterface(interfacels)
              
    def tearDown(self):
          predata = self.getPreConditions()
          f = lambda x :  self.cleandata[x] if x in self.cleandata  else None
          if predata is not None :
                prels = list(map(f,predata))
                self.myservice.handlingDb(prels)
    
    def setCleanData(self,cleandata):
        self.cleandata = cleandata
    
    def getInputData(self):
        data = self.param[5]
        itemdata = data.split("\n")
        jsonstr = "{"+",".join(itemdata) + "}"
        dicdata =  eval(jsonstr)
#         if "memberId" in dicdata:
#             if len(dicdata['memberId']) == 11:
#                    dicdata['memberId'] = UserRegisterService(dicdata['memberId'],dicdata['openid']).getMemberidByPhone()
#                    if dicdata['memberId']  is None:
#                       self.assertFalse(1==1, "memberid为空")
        return dicdata
    
    def getCaseid(self):
        return self.param[0]
    
    def getTestPoint(self):
        return self.param[2]
    
    def getExpectData(self):
        itemdata = []
        data = self.param[6]
        if data is not None and data != "":
               itemdata = data.split("\n")
        f = lambda x : x.split("=")[1]
        lsret = list(map(f,itemdata))
        return lsret
    
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
        return "%s.%s_%s" % (self.__interfaceName__+"--"+self.param[0],self.param[0],self.param[2])
#     return "%s.%s_%s" % (self.__interfaceName__+"--"+self.param[0],self.param[0],self.param[4]+"--"+self.param[2])
#     def __repr__(self):
#         return "<%s testMethod=%s>" % \
#                (self.param[1], self.param[0])
#     def __str__(self):
#         return "%s (%s)" % (self.param[1], self.param[0])
#####################################################
##-testcase
#####################################################
class TestOneZgr(ParametrizedTestCase):
    __interfaceName__ = "baomingzgr"
#     def __init__(self,num):
#         self.num = num
    def test_something(self):
        #print 'param =', self.param
        self.assertEqual(1, 1)

    def test_something_else(self):
        self.assertEqual(2, 2)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTestCase.parametrize(TestOneZgr, params={"test_something":[6,22,33]}))
    suite.addTest(ParametrizedTestCase.parametrize(TestOneZgr, params={"test_something_else":[6,22,33]}))
    unittest.TextTestRunner(verbosity=2).run(suite)