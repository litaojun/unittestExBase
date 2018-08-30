#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年7月8日

@author: ｌｉｔａｏｊｕｎ
'''

import csv,os
from .fileOper import walk_dir_test
from .excelOper import excel_table_byindex
casehear = ("caseid","interfaceName","testPoint","preConditions","operationSteps","testData","expectedResult","actualResult")

#===============================================================================
# csvReadToDict
# filepath 用例文件绝对文件(如D:\\litaojun\\workspace\\a\\unittestExtend\\testcase\\admin\\baoming\\testcase-baoming.csv)
# desc 根据用例文件绝对路径，读取用例数据，返回Dict用例数据{"methonName":[[测试用例],[测试用例]]}
# return
# {  'caocao': [
#                      ['bestvprop_add_6', 'baoming', '\xe5\x85\xa5\xe5\xba\x93\xe5\xa4\xb1\xe8\xb4\xa5-\xe9\x9d\x9e\xe7\xa9\xba\xe6\x95\xb0\xe6\x8d\xae\xe9\xaa\x8c\xe8\xaf\x81-\xe7\xbc\xba\xe5\xb0\x91status\xe5\x8f\x82\xe6\x95\xb0', 'null', 'caocao', '"uuid":"211177777199999915"\n"mobileNo":"18963339931"\n"memberNo":"18963339931"\n"nick":" \xe4\xb8\x89\xe5\x9b\xbd\xe6\x9d\x80"\n"name":" \xe6\x9d\x8e\xe6\xb6\x9b\xe5\x86\x9b"\n"sex":"1"\n"address":"\xe9\x98\xbf\xe8\x90\xa8\xe5\xbe\xb7\xe6\xb3\x95\xe5\xb8\x88\xe6\x89\x93\xe5\x8f\x91\xe6\x96\xaf\xe8\x92\x82\xe8\x8a\xac "', 'code:000101', 'null']
#                     ,['bestvprop_add_7', 'baoming', 'bestv\xe6\x95\xb0\xe6\x8d\xae\xe6\xad\xa3\xe5\xb8\xb8\xe5\x85\xa5\xe5\xba\x93-\xe9\x9d\x9e\xe7\xa9\xba\xe6\x95\xb0\xe6\x8d\xae\xe9\xaa\x8c\xe8\xaf\x81-\xe9\x9d\x9e\xe7\xa9\xba\xe5\x8f\x82\xe6\x95\xb0\xe5\x85\xa8\xe9\x83\xa8\xe7\xbc\xba\xe5\xb0\x91', 'null', 'caocao', '"uuid":"991121112225ffss"\n"status":"1"', 'code:000000', 'null'], ['bestvprop_add_21', 'baoming', '\xe5\x85\xa5\xe5\xba\x93\xe5\xa4\xb1\xe8\xb4\xa5-\xe5\x8f\x82\xe6\x95\xb0\xe6\xa0\xbc\xe5\xbc\x8f\xe9\xaa\x8c\xe8\xaf\x81-haveHouse\xe9\x94\x99\xe8\xaf\xaf', 'null', 'caocao', '"uuid":"211177777199919945"\n"mobileNo":"18963349632"\n"status":"1"\n"memberNo":"18963349632"\n"nick":" \xe4\xb8\x89\xe5\x9b\xbd\xe6\x9d\x80"\n"name":" \xe6\x9d\x8e\xe6\xb6\x9b\xe5\x86\x9b"\n"sex":"1"\n"address":"\xe9\x98\xbf\xe8\x90\xa8\xe5\xbe\xb7\xe6\xb3\x95\xe5\xb8\x88\xe6\x89\x93\xe5\x8f\x91\xe6\x96\xaf\xe8\x92\x82\xe8\x8a\xac "\n"memberStatus":"001002"\n"autoRenewStatus":"002002"\n"payRoad":"003005"\n"level":"004005"\n"userType":"005002"\n"bloodType":"006005"\n"constellation":"007012"\n"education":"008006"\n"marryInfo":"010006"\n"haveHouse":"013007"', 'code:000102', 'null']
#              ]  ,
#    'zugeliang': [
#                  ['bestvprop_add_9', 'baoming', '\xe5\x85\xa5\xe5\xba\x93\xe5\xa4\xb1\xe8\xb4\xa5-\xe5\x8f\x82\xe6\x95\xb0\xe6\xa0\xbc\xe5\xbc\x8f\xe9\xaa\x8c\xe8\xaf\x81-\xe6\x89\x8b\xe6\x9c\xba\xe5\x8f\xb7\xe9\x94\x99\xe8\xaf\xaf', 'null', 'zugeliang', '"uuid":"211177777199999915"\n"mobileNo":"11916899931"\n"status":"1"\n"memberNo":"11916899931"\n"nick":" \xe4\xb8\x89\xe5\x9b\xbd\xe6\x9d\x80"\n"name":" \xe6\x9d\x8e\xe6\xb6\x9b\xe5\x86\x9b"\n"sex":"1"\n"address":"\xe9\x98\xbf\xe8\x90\xa8\xe5\xbe\xb7\xe6\xb3\x95\xe5\xb8\x88\xe6\x89\x93\xe5\x8f\x91\xe6\x96\xaf\xe8\x92\x82\xe8\x8a\xac "', 'code:000102', 'null'], 
#                  ['bestvprop_add_10', 'baoming', '\xe5\x85\xa5\xe5\xba\x93\xe5\xa4\xb1\xe8\xb4\xa5-\xe5\x8f\x82\xe6\x95\xb0\xe6\xa0\xbc\xe5\xbc\x8f\xe9\xaa\x8c\xe8\xaf\x81-sex\xe9\x94\x99\xe8\xaf\xaf', 'null', 'zugeliang', '"uuid":"221177777199199915"\n"mobileNo":"18913339932"\n"status":"1"\n"memberNo":"18913339932"\n"nick":" \xe4\xb8\x89\xe5\x9b\xbd\xe6\x9d\x80"\n"name":" \xe6\x9d\x8e\xe6\xb6\x9b\xe5\x86\x9b"\n"sex":"9"\n"address":"\xe9\x98\xbf\xe8\x90\xa8\xe5\xbe\xb7\xe6\xb3\x95\xe5\xb8\x88\xe6\x89\x93\xe5\x8f\x91\xe6\x96\xaf\xe8\x92\x82\xe8\x8a\xac "', 'code:000102', 'null'],
#              }
#    ...
# }
#===============================================================================
def csvReadToDict(filepath):
    with open(filepath) as csvfile:
         reader = csv.DictReader(csvfile)
         rtdict = {}
         for row in reader:
             f = lambda x : row[x]
             xcurl = map(f,casehear)
             methodname = xcurl[4]
             if not rtdict.has_key(methodname) :
                 rtdict[methodname] = []
             rtdict[methodname].append(xcurl)
         return rtdict
     
def excelReadToDict(filepath):
    #with open(filepath) as excelfile:
         #reader = csv.DictReader(excelfile)
         #print "filepath=%s" % filepath
         reader = excel_table_byindex(filepath)
         interfaceName = reader[0][casehear[1]]
         rtdict = {}
         for row in reader:
             f = lambda x : row[x]
             xcurl = list(map(f,casehear))
             methodname = xcurl[4]
             xcurl.append(filepath)
             #if not rtdict.has_key(methodname) :
             if not methodname in rtdict:
                 rtdict[methodname] = []
             rtdict[methodname].append(xcurl)
         return interfaceName,rtdict
     
     
#===============================================================================
# dictToInfaceDict
# casedict  Dict用例数据{"methonName":[[测试用例],[测试用例]],...}，如下
                # {  'caocao': [
                #                      ['bestvprop_add_6', 'baoming', '\xe5\x85\xa5\xe5\xba\x93\xe5\xa4\xb1\xe8\xb4\xa5-\xe9\x9d\x9e\xe7\xa9\xba\xe6\x95\xb0\xe6\x8d\xae\xe9\xaa\x8c\xe8\xaf\x81-\xe7\xbc\xba\xe5\xb0\x91status\xe5\x8f\x82\xe6\x95\xb0', 'null', 'caocao', '"uuid":"211177777199999915"\n"mobileNo":"18963339931"\n"memberNo":"18963339931"\n"nick":" \xe4\xb8\x89\xe5\x9b\xbd\xe6\x9d\x80"\n"name":" \xe6\x9d\x8e\xe6\xb6\x9b\xe5\x86\x9b"\n"sex":"1"\n"address":"\xe9\x98\xbf\xe8\x90\xa8\xe5\xbe\xb7\xe6\xb3\x95\xe5\xb8\x88\xe6\x89\x93\xe5\x8f\x91\xe6\x96\xaf\xe8\x92\x82\xe8\x8a\xac "', 'code:000101', 'null']
                #                     ,['bestvprop_add_7', 'baoming', 'bestv\xe6\x95\xb0\xe6\x8d\xae\xe6\xad\xa3\xe5\xb8\xb8\xe5\x85\xa5\xe5\xba\x93-\xe9\x9d\x9e\xe7\xa9\xba\xe6\x95\xb0\xe6\x8d\xae\xe9\xaa\x8c\xe8\xaf\x81-\xe9\x9d\x9e\xe7\xa9\xba\xe5\x8f\x82\xe6\x95\xb0\xe5\x85\xa8\xe9\x83\xa8\xe7\xbc\xba\xe5\xb0\x91', 'null', 'caocao', '"uuid":"991121112225ffss"\n"status":"1"', 'code:000000', 'null'], ['bestvprop_add_21', 'baoming', '\xe5\x85\xa5\xe5\xba\x93\xe5\xa4\xb1\xe8\xb4\xa5-\xe5\x8f\x82\xe6\x95\xb0\xe6\xa0\xbc\xe5\xbc\x8f\xe9\xaa\x8c\xe8\xaf\x81-haveHouse\xe9\x94\x99\xe8\xaf\xaf', 'null', 'caocao', '"uuid":"211177777199919945"\n"mobileNo":"18963349632"\n"status":"1"\n"memberNo":"18963349632"\n"nick":" \xe4\xb8\x89\xe5\x9b\xbd\xe6\x9d\x80"\n"name":" \xe6\x9d\x8e\xe6\xb6\x9b\xe5\x86\x9b"\n"sex":"1"\n"address":"\xe9\x98\xbf\xe8\x90\xa8\xe5\xbe\xb7\xe6\xb3\x95\xe5\xb8\x88\xe6\x89\x93\xe5\x8f\x91\xe6\x96\xaf\xe8\x92\x82\xe8\x8a\xac "\n"memberStatus":"001002"\n"autoRenewStatus":"002002"\n"payRoad":"003005"\n"level":"004005"\n"userType":"005002"\n"bloodType":"006005"\n"constellation":"007012"\n"education":"008006"\n"marryInfo":"010006"\n"haveHouse":"013007"', 'code:000102', 'null']
                #              ]  ,
                #    'zugeliang': [
                #                  ['bestvprop_add_9', 'baoming', '\xe5\x85\xa5\xe5\xba\x93\xe5\xa4\xb1\xe8\xb4\xa5-\xe5\x8f\x82\xe6\x95\xb0\xe6\xa0\xbc\xe5\xbc\x8f\xe9\xaa\x8c\xe8\xaf\x81-\xe6\x89\x8b\xe6\x9c\xba\xe5\x8f\xb7\xe9\x94\x99\xe8\xaf\xaf', 'null', 'zugeliang', '"uuid":"211177777199999915"\n"mobileNo":"11916899931"\n"status":"1"\n"memberNo":"11916899931"\n"nick":" \xe4\xb8\x89\xe5\x9b\xbd\xe6\x9d\x80"\n"name":" \xe6\x9d\x8e\xe6\xb6\x9b\xe5\x86\x9b"\n"sex":"1"\n"address":"\xe9\x98\xbf\xe8\x90\xa8\xe5\xbe\xb7\xe6\xb3\x95\xe5\xb8\x88\xe6\x89\x93\xe5\x8f\x91\xe6\x96\xaf\xe8\x92\x82\xe8\x8a\xac "', 'code:000102', 'null'], 
                #                  ['bestvprop_add_10', 'baoming', '\xe5\x85\xa5\xe5\xba\x93\xe5\xa4\xb1\xe8\xb4\xa5-\xe5\x8f\x82\xe6\x95\xb0\xe6\xa0\xbc\xe5\xbc\x8f\xe9\xaa\x8c\xe8\xaf\x81-sex\xe9\x94\x99\xe8\xaf\xaf', 'null', 'zugeliang', '"uuid":"221177777199199915"\n"mobileNo":"18913339932"\n"status":"1"\n"memberNo":"18913339932"\n"nick":" \xe4\xb8\x89\xe5\x9b\xbd\xe6\x9d\x80"\n"name":" \xe6\x9d\x8e\xe6\xb6\x9b\xe5\x86\x9b"\n"sex":"9"\n"address":"\xe9\x98\xbf\xe8\x90\xa8\xe5\xbe\xb7\xe6\xb3\x95\xe5\xb8\x88\xe6\x89\x93\xe5\x8f\x91\xe6\x96\xaf\xe8\x92\x82\xe8\x8a\xac "', 'code:000102', 'null'],
                #              }
                #    ...
                # }  
#desc  将 Dict用例数据{"methonName":[[测试用例],[测试用例]],...}  转换为   {"interfaceName":{{"methonName":[[测试用例],[测试用例]],...}}}
#return
    
#===============================================================================
def dictToInfaceDict(casedict = {}):
    infaceDict = {}
    valueslist = list(casedict.values())
    valuex = valueslist[0][0][1]
    infaceDict[valuex] = casedict
    return infaceDict

      
def a():
    pass
    
if __name__ == '__main__':
    pathcase = os.path.abspath("../../../../"+"\\testcase")
    #print pathcase
#     
#     casedict = csvReadToDict(filepath = pathcase + "\\" + "testcase.csv" )
#     print casedict
    filepaths = walk_dir_test(pathcase)
    #print filepaths
    func = lambda x: csvReadToDict(x)
    funcm = lambda x: dictToInfaceDict(x)
    casedictlist = map(func,filepaths)
    #print casedictlist
    x = map(funcm,casedictlist)
    #print x