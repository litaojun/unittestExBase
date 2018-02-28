#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017

@author: li.taojun
'''
import unittest
from opg.unit.parametrized import ParametrizedTestCase
from opg.util.loadModul import getModul,getModulByabspath
from opg.util.testcaseTool import  creatTestCaseDataByPath,creatTestCaseDataByFile
from opg.unit.testLoadFromModul import loadTestClassFromModules,tranListClassToDict
from opg.unit import HTMLTestRunner
import sys
from opg.util.isSystemType import splict,getPlatfromType

def runTest(moduleabspath='D:\\litaojun\\workspace\\jenkinsPython'):
    #moduls = getModul(path='../../../../',sign="Test")
    sys.path.append(moduleabspath)
    print(sys.path)
    #获取所有测试类模块
    moduls = getModulByabspath(path=moduleabspath,sign="Test")
    print("moduls="+str(list(moduls)))
    #重模块中提取所有测试类（（继承了ParametrizedTestCase））
    cls = loadTestClassFromModules(moduls)
    print("cls="+str(cls))
    #将测试类（继承了ParametrizedTestCase）转换为DICT，其中键值为对应的接口名称
    dictCls = tranListClassToDict(cls)
    print(str(dictCls))
    #通过文件路径获取用例数据
    casedict = creatTestCaseDataByPath(path=moduleabspath)
    print("casedict="+str(casedict))
    #new一个测试套件，通过测试数据和测试类组合成测试用例TestCase，加入到测试套件中
    suites = unittest.TestSuite()
    for casets in casedict:
        infaces = casets.keys()
        for infacename in infaces:
            #if dictCls.has_key(infacename):
            if infacename in dictCls:
               testclass = dictCls[infacename]
               suites.addTest(ParametrizedTestCase.parametrize(testclass, casets[infacename]))
            else:
               print("%s接口对于的类不存在" % infacename)
    #print "suites.tests=",suites._tests
    HtmlFile = moduleabspath+splict+"testresult"+splict+"HTMLtemplate.html"
    #print "HtmlFile = %s" % HtmlFile
    #print HtmlFile
    fp = open(HtmlFile, "wb")
    #new一个Runner
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"UOP-小红巢测试报告", description=u"用例测试情况")
    unitresult = runner.run(suites)
    #unitresult = unittest.TextTestRunner(verbosity=2).run(suites)
    return unitresult

def runTestOneCls(casefilepath='D:\\litaojun\\workspace\\jenkinsPython',testclse=None,moduleabspath=""):
    casedictcls = creatTestCaseDataByFile(casefilepath)
    #print casedictcls
    suites = unittest.TestSuite()
    print(casedictcls)
    casedict = casedictcls[testclse.__interfaceName__]
    suites.addTest(ParametrizedTestCase.parametrize(testclse, casedictcls[testclse.__interfaceName__]))
    HtmlFile = moduleabspath + splict + "testresult" + splict + "HTMLtemplate.html"
    #print "HtmlFile = %s" % HtmlFile
    #print HtmlFile
    fp = open(HtmlFile, "wb")
    #new一个Runner
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"小红巢测试报告", description=u"用例测试情况")
    unitresult = runner.run(suites)

if __name__ == '__main__':
    runTest("D:\\litaojun\\workspace\\uopweixinInterface")