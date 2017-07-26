#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年7月9日

@author: ｌｉｔａｏｊｕｎ
'''
import os
from fileOper import walk_dir_test
from opg.util.csvtools import  csvReadToDict, dictToInfaceDict
from isSystemType import splict,getPlatfromType
s = splict
print "s=",s
#path  测试用例文件所在根目录
#desc  读取相对路径path目录下的所有测试用例，并将测试用例转换为{"interfacename":{"method":[["caseid","interfaceName","testPoint","preConditions","operationSteps","testData","expectedResult","actualResult"][]...[]]}}格式
def creatTestCaseByPath(path="../../../../"):
    #获取相对path所在的绝对路径
    #pathcase = os.path.abspath(path+"\\"+"testcase")
    pathcase = path+s+"testcase"
    filepaths = walk_dir_test(pathcase)
    func = lambda x: csvReadToDict(x)
    funcm = lambda x: dictToInfaceDict(x)
    casedictlist = map(func,filepaths)
    infaceDict = map(funcm,casedictlist)
    return infaceDict


if __name__ == '__main__':
    casedict = creatTestCaseByPath()
    print casedict