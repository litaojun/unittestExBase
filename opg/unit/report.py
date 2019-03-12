import pymysql
from opg.util.dbtools import DbManager, Database
from xml.sax import saxutils
from opg.util.timeTool import getNowTime


def getDbManger():
    return Database()

# 更新指定计划的测试结果


def updateTestResultToDb(testResult=None,
                         projectName=None,
                         token=None,
                         planId=None):
    dbManager = getDbManger()
    processSql = "update test_run_process set status=2 where projectname = '%s' and token = '%s';" % (
        projectName, token)
    result_list = testResult.result
    for n, t, o, e in result_list:
        caseResultDic = {}
        caseResultDic['result_sign'] = n
        caseResultDic['testcaseid'] = t.getCaseid()
        caseResultDic["planId"] = planId
        updateSql = "update test_case_record r set r.result_sign = %(result_sign)s where r.plan_id = %(planId)s and r.testcaseid = '%(testcaseid)s';" % caseResultDic
        dbManager.updateData(sql=updateSql, dbName="ltjtest")
    dbManager.updateData(sql=processSql, dbName="ltjtest")

# 将新执行的测试结果写入数据库


def writeTestResultToDb(testResult=None,
                        title=u"Steam测试报告",
                        description=u"用例测试情况",
                        token="sss"):
    dbManager = getDbManger()
    result_list = testResult.result
    nowdatestr = getNowTime()
    plandict = {
        "plantime": nowdatestr,
        "projectname": title,
        "description": description
    }
    processSql = "update test_run_process set status=2,endtime = '%s' where projectname = '%s' and token = '%s';" % (
        nowdatestr, title, token)
    print("proccesSql = %s" % processSql)
    plansqlStr = "insert into test_plan(plantime,projectname,description) values('%(plantime)s','%(projectname)s','%(description)s') ; " % plandict
    print("plansqlStr = %s" % plansqlStr)

    dbManager.insertData(sql=plansqlStr, dbName="ltjtest")
    planidStr = "select max(id) id from test_plan;"
    idrst = dbManager.queryAll(sql=planidStr, dbName="ltjtest")
    id = idrst[0][0]

    # 更新planId到test_run_process表
    updateProceeSql = "update test_run_process p set p.planId = %d where p.token = '%s';" % (
        id, token)
    dbManager.updateData(sql=updateProceeSql, dbName="ltjtest")
    # n = 异常，错误，成功,
    # t = 测试用例对象 TestCase
    # o = ,
    #e = 异常信息
    for n, t, o, e in result_list:
        caseResultDic = {}
        caseResultDic['result_sign'] = n
        caseResultDic['plan_id'] = id
        caseResultDic['classname'] = t.__class__
        caseResultDic['interfacename'] = "https://uat-steam-api.opg.cn" + \
            t.__interfaceName__
        caseResultDic['testcaseid'] = t.getCaseid()
        caseResultDic['testpoint'] = t.getTestPoint()
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
        dbManager.insertData(sql=insertSql, dbName="ltjtest")
    dbManager.updateData(sql=processSql, dbName="ltjtest")
    # DbManager.closeDbConn()
