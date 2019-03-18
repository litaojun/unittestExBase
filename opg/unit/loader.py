import os
import unittest
from ruamel import yaml
import collections
from opg.util.dynload import Dynload
import sys
from opg.util.fileOper import walk_absdir_modul_file, walk_dir_test
from opg.unit.parametrized import ParametrizedTestCase


def initAllTestCase(casePath=None):
    if casePath is None:
        casePath = os.getcwd()
    testCase = creatTestCaseDataByYmlPath(path=casePath)
    return testCase


def creatTestCaseDataByYmlPath(path=None, sign="s"):
    if path is None:
        path = os.getcwd()
    pathcase = path + os.sep + "steamcase"
    filepaths = walk_dir_test(pathcase, sign=sign, endstr='.yml')
    testcaseDict = {}
    for casedict in list(map(loadYmlToTestcaseByFilepath, filepaths)):
        for interfaceName in casedict:
            testcaseDict[interfaceName] = casedict[interfaceName]
    return testcaseDict


def loadYmlToTestcaseByFilepath(filePath=None):
    ymldata = loadYamlFileData(filePath=filePath)
    tdict = collections.defaultdict(lambda: {})
    for infsTestcases in ymldata["testcases"]:
        interfaceName = infsTestcases["interfaceName"]
        tdict[interfaceName] = collections.defaultdict(lambda: [])
        for case in infsTestcases["case"]:
            preConditions = case.get("preConditions", "")
            operationSteps = case["operationSteps"]
            expectedResult = case["expectedResult"]
            for data in case["testData"]:
                testPoint = data["testPoint"]
                caseid = data["caseid"]
                tdict[interfaceName][operationSteps].append(
                    [caseid, interfaceName, testPoint, preConditions, operationSteps, data, expectedResult])
    return tdict


def loadYamlFileData(filePath=None):
    #
    #sprint("filepath = %s " % filePath)
    with open(filePath, 'r', encoding="utf-8") as f:
        try:
            ymldata = yaml.safe_load(f.read())
            return ymldata
        except yaml.YAMLError as exc:
            print(exc)


def initAllTestClass():
    moduleabspath = os.getcwd()
    sys.path.append(moduleabspath)
    # print(sys.path)
    # 获取所有测试类模块
    moduls = getModulByabspath(path=moduleabspath, sign="Test")
    # print("moduls="+str(list(moduls)))
    # 重模块中提取所有测试类（（继承了ParametrizedTestCase））
    cls = loadTestClassFromModules(moduls)
    dictCls = tranListClassToDict(cls)
    return dictCls


def getModulByabspath(path='', sign="load"):
    # 定义lambda函数，将com\\bestv\\kafka\\kafkacon转换为(.com.bestv.kafka,.kafkacon)
    def lfunc(x): return os.path.splitext(
        os.path.basename(x.replace(os.sep, ".")))
    # mfunc = lambda  x : x.replace(s,".")
    # 定义lambda函数，将(x="com.bestv.kafka.kafkacon",y=[com.bestv.kafka,])加载为模块
    def nfunc(x, y): return Dynload(x, imp_list=y).getobject()
    # 通过相对路径获取绝对路径
    #curpath =  os.path.abspath(path)
    curpath = path
    # 加载绝对路径下的所有模块文件，格式["com\\bestv\\kafka\\kafkacon",]
    lsn = walk_absdir_modul_file(curpath, sign=sign, endstr=".py")
    a = map(lfunc, lsn)
    # 将(.com.bestv.kafka,.kafkacon)转换为(com.bestv.kafka.kafkacon,com.bestv.kafka)
    d = tuple([(x[1:] + y, [x[1:]]) for x, y in a])
    # 将(com.bestv.kafka.kafkacon,com.bestv.kafka)转换为模块
    mdlist = list(map(nfunc, [a[0] for a in d], [a[1] for a in d]))
    return mdlist


# ===============================================================================
# 从模块中获取所有测试测试类（继承了ParametrizedTestCase）
#
# ===============================================================================
def loadTestClassFromModules(modules):
    testClass = []
    for mod in modules:
        tcls = loadTestClassFromModule(mod)
        if tcls is not None:
            testClass.append(tcls)
    return testClass

# ===============================================================================
# 将测试类（继承了ParametrizedTestCase）转换为DICT，其中键值为对应的接口名称
# ===============================================================================


def tranListClassToDict(testClass=[]):
    def func(x): return (
        x.__interfaceName__, x) if hasattr(
        x, "__interfaceName__") else None
    tuplea = map(func, testClass)
    di = {}
    for t in tuplea:
        if t is not None:
            di[t[0]] = t[1]
    return di

# ===============================================================================
# 从模块中获取所有测试测试类（继承了ParametrizedTestCase）
#
# ===============================================================================


def loadTestClassFromModules(modules):
    testClass = []
    for mod in modules:
        tcls = loadTestClassFromModule(mod)
        if tcls is not None:
            testClass.append(tcls)
    return testClass


# ===============================================================================
# loadTestClassFromModule
# module <module 'com.tao.opg.util.dynload' from 'D:\litaojun\workspace\unittestExtend\com\tao\opg\util\dynload.pyc'>
# desc case.TestCase
# return
# ===============================================================================
def loadTestClassFromModule(module, use_load_tests=True):
    """Return a suite of all tests cases contained in the given module"""
    tests = None
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and issubclass(obj, ParametrizedTestCase) and str(obj) != str(
                ParametrizedTestCase) and str(obj) != "<class 'uopweixin.util.parametrizedCase.ParametrizedCase'>":
            if obj.__name__.endswith("Test"):
                tests = obj
    return tests


def genAllTestCase(allCase, allTestClass):
    suites = unittest.TestSuite()
    for infacename in allCase:
        if infacename in allTestClass:
            testclass = allTestClass[infacename]
            suites.addTest(
                ParametrizedTestCase.parametrize(
                    testclass, allCase[infacename]))
        else:
            print("%s接口对应的类不存在" % infacename)
    return suites

# 根据接口名称和用例ID构造用例


def genTestCaseByInterfaceOrCaseIds(allCase=None,
                                    allTestClass=None,
                                    interfaceName=None,
                                    caseIds=[]):
    genAllTestCase(allCase=allCase,allTestClass=allTestClass)
    suites = unittest.TestSuite()
    testclass = allTestClass[interfaceName]
    testCases = allCase[interfaceName]
    for methonName in testCases:
        caseList = testCases[methonName]
        for testcase in caseList:
            if caseIds is not None and len(caseIds) >= 1:
                if testcase[0] in caseIds:
                    suites.addTest(testclass(methonName, testcase))
            else:
                suites.addTest(testclass(methonName, testcase))
    return suites
