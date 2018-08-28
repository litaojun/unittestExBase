#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017

@author: li.taojun
'''
import unittest
from opg.unit.parametrized import ParametrizedTestCase
from opg.util.loadModul import getModulByabspath
from opg.util.testcaseTool import  creatTestCaseDataByPath,creatTestCaseDataByFile
from opg.unit.testLoadFromModul import loadTestClassFromModules,tranListClassToDict
from opg.unit import HTMLTestRunner
import sys,os
from opg.util.isSystemType import splict
from opg.util.dbtools import DbManager
from xml.sax import saxutils
from opg.util.timeTool import getNowTime
import uuid,time
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
    for casets in casedict:
        infaces = casets.keys()
        for infacename in infaces:
            #if dictCls.has_key(infacename):
            if infacename in dictCls:
               testclass = dictCls[infacename]
               suites.addTest(ParametrizedTestCase.parametrize(testclass, casets[infacename]))
            else:
               print("%s接口对应的类不存在" % infacename)
    #print "suites.tests=",suites._tests
    HtmlFile = moduleabspath+splict+"testresult"+splict+"HTMLtemplate.html"
    fp = open(HtmlFile, "wb")
    #new一个Runner
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=title, description=description)
    unitresult = runner.run(suites)
    #unitresult = unittest.TextTestRunner(verbosity=2).run(suites)
    writeTestResultToDb(testResult = unitresult,title=title,description=description,token=token)
    return unitresult

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
    DbManager.cleanDB()
    dbManager = DbManager(host="steam-uat-default.crbcfaeazoqe.rds.cn-northwest-1.amazonaws.com.cn",
                          user="root",
                          password="Bestv001!",
                          dbname="ltjtest",
                          port=3306)
    return dbManager


def getRunTestTokenId(projectname = "",starTime="sss"):
    dbManager = getDbManger()
    starttime = getNowTime()
    tokenId = uuid.uuid4()
    sqlstr = "insert into test_run_process(token,starttime,status,projectname) value('%s','%s',1,'%s')" % (tokenId,starttime,projectname)
    dbManager.insertData(sql_insert=sqlstr)
    return  tokenId

def queryStateByTokenPro(projectName = "",token = ""):
    dbManager = getDbManger()
    keyls = ["id", "starttime", "status", "endtime", "projectname"]
    querySql = """select  id, starttime, status, endtime, projectname 
                      from test_run_process p 
                      where p.projectname = "%s" 
                            and  p.token = "%s";""" % (projectName, token)
    dataList = dbManager.queryAll(sql=querySql)
    if dataList is not None and len(dataList) > 0:
        return dict(zip(keyls,dataList[0]))

def queryTestPlanList(projectName = ""):
    dbManager = getDbManger()
    keyls = ["id", "plantime", "projectname", "description"]
    querySql = """select id, plantime, projectname, description 
                  from test_plan p 
                  where projectname = "%s"   ;""" % projectName
    dataList = dbManager.queryAll(sql=querySql)
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
    dataList = dbManager.queryAll(sql=querySql)
    retList  = [dict(zip(keyls,data)) for data in dataList]
    return retList

def queryTestPlanAllInterfaceName(interfaceName = "",planId = 22,db = None):
    dbManager = getDbManger()
    keyls = ["interfacename", "testcaseid", "testpoint", "result_sign","errordes"]
    querySql = """select  interfacename, testcaseid, testpoint, result_sign, errordes 
                  from test_case_record r	
                  where r.plan_id = %s ;""" % planId
    dataList = dbManager.queryAll(sql=querySql)
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
    dataList = dbManager.queryAll(sql=querySql)
    if dataList is None:
       dataList = []
    retList = [dict(zip(keyls, data)) for data in dataList]
    return retList


def queryPlanDetailByInterfaceName(planId = 22):
    planRecordList = queryTestPlanRecord(planId=planId)
    allRecordList =queryTestPlanAllInterfaceName(planId=planId)
    for planRecord in planRecordList:
        interfaceName = planRecord["interfaceName"]
        interfacePlanRecord = [record for record in allRecordList if record["interfacename"] == interfaceName]
        planRecord["result"] = interfacePlanRecord
    retDict = {}
    retDict["code"] = "000000"
    retDict["testrst"] = planRecordList
    return  retDict




def writeTestResultToDb(testResult = None,
                        title=u"Steam测试报告",
                        description=u"用例测试情况",
                        token="sss"):
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
    dbManager.updateData(processSql)
    plansqlStr = "insert into test_plan(plantime,projectname,description) values('%(plantime)s','%(projectname)s','%(description)s') ; " % plandict
    print("plansqlStr = %s" % plansqlStr)
    # t = plansqlStr % plandict
    # print("t = %s" % t)
    dbManager.insertData(sql_insert=plansqlStr)
    planidStr = "select max(id) id from test_plan;"
    idrst = dbManager.queryAll(sql = planidStr)
    id = idrst[0][0]
    #n = 异常，错误，成功,
    #t = 测试用例对象 TestCase
    #o = ,
    #e = 异常信息
    for n, t, o, e in result_list:
        caseResultDic = {}
        caseResultDic['result_sign'] = n
        caseResultDic['plan_id']      = id
        caseResultDic['classname']    = t.__class__
        caseResultDic['interfacename'] = t.__interfaceName__
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
        caseResultDic['errordes'] = dbManager.conn.escape(script)
        sqlstr = "insert into test_case_record(classname,interfacename,testcaseid,testpoint,plan_id,result_sign,errordes) values(\"%(classname)s\" , '%(interfacename)s','%(testcaseid)s','%(testpoint)s','%(plan_id)s','%(result_sign)s',\"%(errordes)s\")"
        insertSql = sqlstr % caseResultDic
        dbManager.insertData(sql_insert=insertSql)

if __name__ == '__main__':
    runTest("D:\\litaojun\\workspace\\uopweixinInterface")