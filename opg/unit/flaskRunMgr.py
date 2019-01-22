#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017

@author: li.taojun
'''
import unittest
from opg.unit.parametrized import ParametrizedTestCase
from opg.util.loadModul import getModulByabspath
from opg.util.testcaseTool import  creatTestCaseDataByPath,creatTestCaseDataByFile,creatTestCaseDataByYmlPath
from opg.unit.testLoadFromModul import loadTestClassFromModules,tranListClassToDict
from opg.unit import HTMLTestRunner
import pymysql
import sys,os
from opg.util.isSystemType import splict
from opg.util.dbtools import DbManager,Database
from xml.sax import saxutils
from opg.util.timeTool import getNowTime
import uuid

def runTest(moduleabspath='',
            title=u"Steam测试报告",
            description=u"用例测试情况",
            token = "ssss"):
    #moduls = getModul(path='../../../../',sign="Test")
    #writeStartTestToDb(projectname = title,starTime=starTime)
    moduleabspath = os.getcwd()
    sys.path.append(moduleabspath)
    #print(sys.path)
    #获取所有测试类模块
    moduls = getModulByabspath(path=moduleabspath,sign="Test")
    #print("moduls="+str(list(moduls)))
    #重模块中提取所有测试类（（继承了ParametrizedTestCase））
    cls = loadTestClassFromModules(moduls)
    #将测试类（继承了ParametrizedTestCase）转换为DICT，其中键值为对应的接口名称
    dictCls = tranListClassToDict(cls)
    # print(str(dictCls))
    #通过文件路径获取用例数据
    casedict = creatTestCaseDataByPath(path=moduleabspath)
    # print("casedict="+str(casedict))
    #new一个测试套件，通过测试数据和测试类组合成测试用例TestCase，加入到测试套件中
    suites = unittest.TestSuite()
    for infacename in casedict:
            if infacename in dictCls:
               testclass = dictCls[infacename]
               suites.addTest(ParametrizedTestCase.parametrize(testclass, casedict[infacename]))
            else:
               print("%s接口对应的类不存在" % infacename)
    HtmlFile = moduleabspath+splict+"testresult"+splict+"HTMLtemplate.html"
    fp = open(HtmlFile, "wb")
    #new一个Runner
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=title, description=description)
    unitresult = runner.run(suites)
    #unitresult = unittest.TextTestRunner(verbosity=2).run(suites)
    writeTestResultToDb(testResult = unitresult,title=title,description=description,token=token)
    return unitresult

def initAllTestClass():
    moduleabspath = os.getcwd()
    sys.path.append(moduleabspath)
    # print(sys.path)
    # 获取所有测试类模块
    moduls = getModulByabspath(path=moduleabspath, sign="Test")
    # print("moduls="+str(list(moduls)))
    # 重模块中提取所有测试类（（继承了ParametrizedTestCase））
    cls     = loadTestClassFromModules(moduls)
    dictCls = tranListClassToDict(cls)
    return dictCls

def genAllTestCase(allCase,allTestClass):
    suites = unittest.TestSuite()
    for infacename in allCase:
        if infacename in allTestClass:
           testclass = allTestClass[infacename]
           suites.addTest(ParametrizedTestCase.parametrize(testclass, allCase[infacename]))
        else:
            print("%s接口对应的类不存在" % infacename)
    return suites

def genTestCaseByInterfaceOrCaseIds(allCase       = None,
                                    allTestClass  = None,
                                    interfaceName = None,
                                    caseIds       = []):
    suites    = unittest.TestSuite()
    testclass = allTestClass[interfaceName]
    testCases = allCase[interfaceName]
    for methonName in testCases:
        caseList = testCases[methonName]
        for testcase in caseList:
            if testcase[0] in caseIds:
               suites.addTest(testclass(methonName,testcase))
    return suites

def runTestCase(suites      = None ,
                title       = ""   ,
                description = ""   ):
    runner = HTMLTestRunner.HTMLTestRunner(stream      = None,
                                           title       = title,
                                           description = description)
    unitresult = runner.runSteam(suites)
    return unitresult


def runAllTestCase(suites      = None,
                   title       = "",
                   description = "",
                   token       = ""):

    unitresult = runTestCase(suites      = suites,
                             title       = title,
                             description = description)
    writeTestResultToDb(testResult  = unitresult,
                        title       = title,
                        description = description,
                        token       = token)
    return unitresult
def runOneTestcase(suites      = None,
                   planId      = None,
                   token       = None,
                   title       = None,
                   description = None):
    unitresult = runTestCase(suites      = suites,
                             title       = title,
                             description = description)
    updateTestResultToDb(testResult  = unitresult,
                         projectName = title,
                         token       = token,
                         planId      = planId)

def initAllTestCase(casePath = None):
    if casePath is None:
       casePath = os.getcwd()
    #steamTestCase = creatTestCaseDataByPath(path=moduleabspath)
    steamTestCase = creatTestCaseDataByYmlPath(path = casePath)
    return steamTestCase

def runTestOneCls(casefilepath='D:\\litaojun\\workspace\\jenkinsPython',testclse=None,moduleabspath=""):
    basepath = os.getcwd()
    casedictcls = creatTestCaseDataByFile(basepath + casefilepath)
    #print casedictcls
    suites = unittest.TestSuite()
    print(casedictcls)
    casedict = casedictcls[testclse.__interfaceName__]
    suites.addTest(ParametrizedTestCase.parametrize(testclse , casedictcls[testclse.__interfaceName__]))
    HtmlFile = basepath + splict + "testresult" + splict + "HTMLtemplate.html"
    #print "HtmlFile = %s" % HtmlFile
    #print HtmlFile
    fp = open(HtmlFile, "wb")
    #new一个Runner
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"小红巢测试报告", description=u"用例测试情况")
    unitresult = runner.run(suites)
    #writeTestResultToDb(testResult=unitresult)
    return unitresult

def runTestOneTestcaseByCls(casefilepath='D:\\litaojun\\workspace\\jenkinsPython',testclse=None,caseids = [],moduleabspath=""):
    """
    :param casefilepath: 用例路径
    :param testclse:测试类
    :param caseid:用例ID
    :param moduleabspath:模块路径
    :return:
    """
    casedictcls = creatTestCaseDataByFile(casefilepath)
    #print casedictcls
    suites = unittest.TestSuite()
    #print(casedictcls)
    casedict = casedictcls[testclse.__interfaceName__]
    clsSuites = ParametrizedTestCase.parametrize(testclse, casedictcls[testclse.__interfaceName__])
    for curcase in clsSuites:
        curcaseid = curcase.getCaseid()
        if curcaseid in caseids:
            suites.addTest(curcase)
    HtmlFile = moduleabspath+splict+"testresult"+splict+"HTMLtemplate.html"
    fp = open(HtmlFile, "wb")
    #new一个Runner
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"小红巢测试报告", description=u"用例测试情况")
    unitresult = runner.run(suites)
    writeTestResultToDb(testResult=unitresult)
    return unitresult

def getDbManger():
    # DbManager.cleanDB()
    # dbManager = DbManager(host="steam-uat-default.crbcfaeazoqe.rds.cn-northwest-1.amazonaws.com.cn",
    #                       user="root",
    #                       password="Bestv001!",
    #                       dbname="ltjtest",
    #                       port=3306)
    return Database()


def getRunTestTokenId(projectname = "",starTime="sss"):
    dbManager = getDbManger()
    starttime = getNowTime()
    tokenId = uuid.uuid4()
    sqlstr = "insert into test_run_process(token,starttime,status,projectname) value('%s','%s',1,'%s')" % (tokenId,starttime,projectname)
    dbManager.insertData(sql=sqlstr,dbName="ltjtest")
    return  tokenId,starttime

def queryStateByTokenPro(projectName = "",token = ""):
    dbManager = getDbManger()
    keyls = ["id", "starttime", "status", "endtime", "projectname","hourtime","mintime","sectime"]
    querySql = """select  id, starttime, status, endtime, projectname ,HOUR(timediff(endtime , starttime)) hourtime ,minute(timediff(endtime , starttime)) mintime,SECOND(timediff(endtime , starttime)) sectime
                      from test_run_process p 
                      where p.projectname = "%s" 
                            and  p.token = "%s";""" % (projectName, token)
    dataList = dbManager.queryAll(sql = querySql,dbName="ltjtest")
    if dataList is not None and len(dataList) > 0:
            return dict(zip(keyls,dataList[0]))

def queryTestPlanList(projectName = ""):
    dbManager = getDbManger()
    keyls = ["id", "plantime", "projectname", "description"]
    querySql = """select id, plantime, projectname, description 
                  from test_plan p 
                  where projectname = "%s"   ;""" % projectName
    dataList = dbManager.queryAll(sql=querySql,dbName="ltjtest")
    retList  = [dict(zip(keyls,data)) for data in dataList]
    retDict = {}
    retDict["code"] = "000000"
    retDict["listplan"] = retList
    return retDict

def queryTestPlanByInterfaceName(interfaceName = "",planId = 22,db = None):
    dbManager = getDbManger()
    keyls = ["interfacename", "testcaseid", "testpoint", "result_sign","errordes"]
    querySql = """select  interfacename, testcaseid, testpoint, result_sign, errordes 
                  from test_case_record r	
                  where r.plan_id = %s and 
                        r.interfacename = '%s';""" % (planId,interfaceName)
    dataList = dbManager.queryAll(sql=querySql,dbName="ltjtest")
    retList  = [dict(zip(keyls,data)) for data in dataList]
    return retList

def queryAllInterfaceByProjectName(projectName = None):
    dbManager = getDbManger()
    keyls = ["aliasName","interfaceAddr","reqtype","module","mark","reqpath","rsppath"]
    querySql = """select inf.aliasName,inf.interfaceNameAddr,inf.reqtype,inf.module,inf.mark,inf.reqDataPath,inf.rspDataPath 
                    from interface_mgr inf 
                    where inf.projectname = "%s";""" % projectName
    dataList = dbManager.queryAll(sql=querySql,dbName="ltjtest")
    if dataList is None:
        dataList = []
    # for data in dataList:
    #     data[4] = os.path.basename(data[4])
    #     data[5] = os.path.basename(data[5])
    retList = [dict(zip(keyls, data)) for data in dataList]
    retdata = {
                 "code":"000000",
                 "infsList":retList
               }
    return retdata


def queryTestPlanAllInterfaceName(interfaceName = "",planId = 22,db = None):
    dbManager = getDbManger()
    keyls = ["interfacename", "testcaseid", "testpoint", "resultSign","errordes"]
    querySql = """select  interfacename, testcaseid, testpoint, result_sign, errordes 
                  from test_case_record r	
                  where r.plan_id = %s ;""" % planId
    dataList = dbManager.queryAll(sql=querySql,dbName="ltjtest")
    if dataList is None:
        dataList = []
    retList  = [dict(zip(keyls,data)) for data in dataList]
    return retList

def queryTestPlanRecord(planId = 11):
    dbManager = getDbManger()
    keyls = ["interfaceName", "success", "fail", "error", "total"]
    querySql = """select  r.interfacename 'interfaceName',
							CONVERT(sum(case r.result_sign  when '0' then 1 else 0 end) ,SIGNED )  'success',
							CONVERT(sum(case r.result_sign  when '1' then 1 else 0 end),SIGNED )  'fail',
							CONVERT(sum(case r.result_sign  when '2' then 1 else 0 end),SIGNED )  'error',
			                CONVERT(sum(1),SIGNED )  'total'
			        from test_case_record r 
			        where r.plan_id = %s group by r.interfacename;""" % planId
    dataList = dbManager.queryAll(sql=querySql,dbName="ltjtest")
    if dataList is None:
       dataList = []
    retList = [dict(zip(keyls, data)) for data in dataList]
    return retList


def queryPlanDetailByInterfaceName(planId = 22):
    planRecordList = queryTestPlanRecord(planId=planId)
    allRecordList  =  queryTestPlanAllInterfaceName(planId=planId)
    for planRecord in planRecordList:
        interfaceName         = planRecord["interfaceName"]
        interfacePlanRecord   = [record for record in allRecordList if record["interfacename"] == interfaceName]
        planRecord["result"] = interfacePlanRecord
    retDict = {}
    retDict["code"] = "000000"
    retDict["testrst"] = planRecordList
    return  retDict

#更新指定计划的测试结果
def updateTestResultToDb(testResult  = None,
                         projectName = None,
                         token       = None,
                         planId      = None):
    dbManager = getDbManger()
    processSql = "update test_run_process set status=2 where projectname = '%s' and token = '%s';" % ( projectName, token)
    result_list = testResult.result
    for n, t, o, e in result_list:
        caseResultDic = {}
        caseResultDic['result_sign']    = n
        caseResultDic['testcaseid']     = t.getCaseid()
        caseResultDic["planId"]          = planId
        updateSql = "update test_case_record r set r.result_sign = %(result_sign)s where r.plan_id = %(planId)s and r.testcaseid = '%(testcaseid)s';" % caseResultDic
        dbManager.updateData(sql=updateSql,dbName="ltjtest")
    dbManager.updateData(sql=processSql,dbName="ltjtest")

#将新执行的测试结果写入数据库
def writeTestResultToDb(testResult = None,
                        title      = u"Steam测试报告",
                        description= u"用例测试情况",
                        token      = "sss"):
    dbManager   =    getDbManger()
    result_list = testResult.result
    nowdatestr = getNowTime()
    plandict = {
                 "plantime":nowdatestr,
                 "projectname":title,
                 "description":description
                }
    processSql = "update test_run_process set status=2,endtime = '%s' where projectname = '%s' and token = '%s';" %(nowdatestr,title,token)
    print("proccesSql = %s" % processSql)
    plansqlStr = "insert into test_plan(plantime,projectname,description) values('%(plantime)s','%(projectname)s','%(description)s') ; " % plandict
    print("plansqlStr = %s" % plansqlStr)

    dbManager.insertData(sql=plansqlStr,dbName="ltjtest")
    planidStr = "select max(id) id from test_plan;"
    idrst = dbManager.queryAll(sql = planidStr,dbName="ltjtest")
    id = idrst[0][0]

    #更新planId到test_run_process表
    updateProceeSql  = "update test_run_process p set p.planId = %d where p.token = '%s';" % (id ,token)
    dbManager.updateData(sql=updateProceeSql,dbName="ltjtest")
    #n = 异常，错误，成功,
    #t = 测试用例对象 TestCase
    #o = ,
    #e = 异常信息
    for n, t, o, e in result_list:
        caseResultDic = {}
        caseResultDic['result_sign'] = n
        caseResultDic['plan_id']      = id
        caseResultDic['classname']    = t.__class__
        caseResultDic['interfacename'] = "https://uat-steam-api.opg.cn" + t.__interfaceName__
        caseResultDic['testcaseid']     = t.getCaseid()
        caseResultDic['testpoint']      = t.getTestPoint()
        if isinstance(o, str):
            # TODO: some problem with 'string_escape': it escape \n and mess up formating
            # uo = unicode(o.encode('string_escape'))
            # uo    = o.decode('latin-1')
            uo = e
        else:
            uo = o
        if isinstance(e, str):
            # TODO: some problem with 'string_escape': it escape \n and mess up formating
            # ue = unicode(e.encode('string_escape'))
            # ue = e.decode('latin-1')
            ue = e
        else:
            ue = e

        script = "%(output)s" % dict(
                                          output=saxutils.escape(uo + ue),
                                       )
        # caseResultDic['errordes'] = dbManager.conn.escape(script)
        caseResultDic['errordes'] = pymysql.escape_string(script)
        sqlstr = "insert into test_case_record(classname,interfacename,testcaseid,testpoint,plan_id,result_sign,errordes) values(\"%(classname)s\" , '%(interfacename)s','%(testcaseid)s','%(testpoint)s','%(plan_id)s','%(result_sign)s',\"%(errordes)s\")"
        insertSql = sqlstr % caseResultDic
        dbManager.insertData(sql=insertSql,dbName="ltjtest")
    dbManager.updateData(sql=processSql,dbName="ltjtest")
    # DbManager.closeDbConn()

if __name__ == '__main__':
    runTest("D:\\litaojun\\workspace\\uopweixinInterface")