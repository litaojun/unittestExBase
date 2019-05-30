from opg.unit.parametrized import ParametrizedTestCase
from opg.unit.report import writeTestResultToDb, updateTestResultToDb
from opg.unit.loader import loadYmlToTestcaseByFilepath
import os
import unittest
from opg.unit import HTMLTestRunner
writeDir = None
def runOneTestcase(suites=None,
                   planId=None,
                   token=None,
                   title=None,
                   description=None):
    unitresult = runTestCase(suites=suites,
                             title=title,
                             description=description)
    updateTestResultToDb(testResult=unitresult,
                         projectName=title,
                         token=token,
                         planId=planId)


def runTestCase(suites=None,
                title="",
                description=""):
    # global writeDir
    # logDir = genDir()
    # writeDir = writeLog(wtrDir=logDir)
    runner = HTMLTestRunner.HTMLTestRunner(stream=None,
                                           title=title,
                                           description=description)
    unitresult = runner.runSteam(suites)
    return unitresult


def runAllTestCase(suites=None,
                   title="",
                   description="",
                   token=""):
    unitresult = runTestCase(suites=suites,
                             title=title,
                             description=description)
    writeTestResultToDb(testResult=unitresult,
                        title=title,
                        description=description,
                        token=token)
    return unitresult


def runTestOneCls(casefilepath='D:\\litaojun\\workspace\\jenkinsPython',
                  testclse=None,
                  basepath=None):
    if basepath is None:
        basepath = os.getcwd()
    casedictcls = loadYmlToTestcaseByFilepath(basepath + casefilepath)
    # print casedictcls
    suites = unittest.TestSuite()
    print(casedictcls)
    # casedict = casedictcls[testclse.__interfaceName__]
    suites.addTest(ParametrizedTestCase.parametrize(
        testclse, casedictcls[testclse.__interfaceName__]))
    HtmlFile = basepath + os.sep + "testresult" + os.sep + "HTMLtemplate.html"
    fp = open(HtmlFile, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp, title=u"小红巢测试报告", description=u"用例测试情况")
    unitresult = runner.run(suites)
    # writeTestResultToDb(testResult=unitresult)
    return unitresult


def runOneCls(suites=None,
                  basepath=None):
    HtmlFile = basepath + os.sep + "testresult" + os.sep + "HTMLtemplate.html"
    fp = open(HtmlFile, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp, title=u"小红巢测试报告", description=u"用例测试情况")
    unitresult = runner.run(suites)
    # writeTestResultToDb(testResult=unitresult)
    return unitresult
