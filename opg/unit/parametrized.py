#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 
http://blog.csdn.net/jasonwoolf/article/details/47979655
@author: li.taojun
'''

import unittest
class ParametrizedTestCase(unittest.case.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """
    def __init__(self, methodName='runTest', param=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.param = param
    @staticmethod
    def parametrize(testcase_klass, param={}):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        suite = unittest.TestSuite()
        
        testnames = param.keys()
        for name in testnames:
            casels = param[name]
            for onecase in casels:
                 if hasattr(testcase_klass, name):
                     suite.addTest(testcase_klass(name,onecase))
                 else:
                     print "%s类不存在%s方法" % (testcase_klass.__name__,name)
        return suite
    def id(self):
        return "%s.%s_%s" % (self.__interfaceName__+"--"+self.param[1],self.param[0],self.param[4])
    def __repr__(self):
        return "<%s testMethod=%s>" % \
               (self.param[1], self.param[0])
    def __str__(self):
        return "%s (%s)" % (self.param[1], self.param[0])
#####################################################
##-testcase
#####################################################
class TestOneZgr(ParametrizedTestCase):
    __interfaceName__ = "baomingzgr"
    def test_something(self):
        print 'param =', self.param
        self.assertEqual(1, 1)

    def test_something_else(self):
        self.assertEqual(2, 2)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTestCase.parametrize(TestOneZgr, param=42))
    suite.addTest(ParametrizedTestCase.parametrize(TestOneZgr, param=13))
    unittest.TextTestRunner(verbosity=2).run(suite)