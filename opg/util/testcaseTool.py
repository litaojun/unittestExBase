#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年7月9日

@author: ｌｉｔａｏｊｕｎ
'''
import os
from ruamel import yaml
import collections
from opg.util.fileOper import walk_dir_test
from opg.util.csvtools import  excelReadToDict

#path  测试用例文件所在根目录
#desc  读取相对路径path目录下的所有测试用例，并将测试用例转换为{"interfacename":{"method":[["caseid","interfaceName","testPoint","preConditions","operationSteps","testData","expectedResult","actualResult"][]...[]]}}格式
def creatTestCaseDataByPath(path="../../../../"):
    #获取相对path所在的绝对路径
    #pathcase = os.path.abspath(path+"\\"+"testcase")
    pathcase = path + os.sep + "steamcase"
    filepaths = walk_dir_test(pathcase)
    #func = lambda x: csvReadToDict(x)
    func = lambda x: excelReadToDict(x)
    #funcm = lambda x: dictToInfaceDict(x)
    infaceDict = dict(list(map(func,filepaths)))
    #infaceDict = list(map(funcm,casedictlist))
    return infaceDict

def creatTestCaseDataByFile(filepath="../../../../"):
    #获取相对path所在的绝对路径
    func = lambda x: excelReadToDict(x)
    infaceDict = dict([func(filepath)])
    return infaceDict

def creatTestCaseDataByYmlPath(path = None,sign = "s"):
    #获取相对path所在的绝对路径
    #pathcase = os.path.abspath(path+"\\"+"testcase")
    if path is None:
       path   = os.getcwd()
    pathcase  = path + os.sep + "steamcase"
    filepaths = walk_dir_test(pathcase,sign = sign,endstr = '.yml')
    testcaseDict = {}
    for casedict in list(map(loadYmlToTestcaseByFilepath,filepaths)):
        for interfaceName in casedict:
            testcaseDict[interfaceName] = casedict[interfaceName]
    return testcaseDict


def loadYmlToTestcaseByFilepath(filePath = None):
    """
        :param filePath:
        :return:
    """
    #filePath = "D:\litaojun\steamyml\matchAppleTestCase.yml"
    ymldata = loadYamlFileData(filePath=filePath)
    # print(ymldata)
    tdict = collections.defaultdict(lambda: {})
    for infsTestcases in ymldata["testcases"]:
        interfaceName = infsTestcases["interfaceName"]
        tdict[interfaceName] = collections.defaultdict(lambda: [])
        for case in infsTestcases["case"]:
            preConditions  = case.get("preConditions", "")
            operationSteps = case["operationSteps"]
            expectedResult = case["expectedResult"]
            for data in case["testData"]:
                testPoint = data["testPoint"]
                caseid    = data["caseid"]
                tdict[interfaceName][operationSteps].append(
                    [caseid, interfaceName, testPoint, preConditions, operationSteps, data, expectedResult])
    return tdict

# def loadYamlFileData(filePath = None):
#     #sprint("filepath = %s " % filePath)
#     with open(filePath, 'r',encoding="utf-8") as f:
#         ymldata = yaml.load(f.read())
#         #print("ymldata = %s " % ymldata)
#         return ymldata

def tranXlsToYmlFile(casedict = None):
    #casedict = creatTestCaseDataByPath()
    for interfaceName in casedict:
        path = os.getcwd() + os.sep + "steamcase"
        d = collections.defaultdict(lambda: [])
        filepath = path + os.sep + interfaceName.replace("/","") + "s.yml"
        tmdt = {
                    "interfaceName": interfaceName,
                    "case": []
                }
        for method in casedict[interfaceName]:
            for casedata in casedict[interfaceName][method]:
                testData = tranDataTodict(casedata[5])
                testData["caseid"]     = casedata[0]
                testData["testPoint"]  = casedata[2]
                case = {
                          "testPoint"     : casedata[2],
                          "preConditions" : casedata[3].split("\n"),
                          "operationSteps": casedata[4],
                          "testData"       : [testData],
                          "expectedResult": tranDataTodict(casedata[6])
                       }
                tmdt["case"].append(case)
            d["testcases"].append(tmdt)
        print("d = " + str(d))
        dumpDataToYmlFile(filePath = filepath ,data = d)

def loadYamlFileData(filePath = None):
    #sprint("filepath = %s " % filePath)
    with open(filePath, 'r',encoding="utf-8") as f:
        try:
            ymldata = yaml.safe_load(f.read())
            return ymldata
        except yaml.YAMLError as exc:
            print(exc)


def dumpDataToYmlFile(filePath = None,data = None):
    data = dict(data)
    with open(filePath, 'w', encoding="utf-8") as f:
         yaml.dump(data,f,Dumper=yaml.RoundTripDumper, default_flow_style=False, allow_unicode=True)

def tranDataTodict(data = None):
    jsonstr = "{" + ",".join(data.split("\n")) + "}"
    dicdata = None
    try:
        dicdata = eval(jsonstr)
    except Exception as ex:
        print(ex)
        print(jsonstr)
    return dicdata




if __name__ == '__main__':
    #casedict = creatTestCaseDataByPath()
    casedict = creatTestCaseDataByYmlPath(path = "D:\litaojun\steamyml")
    print(casedict)
    casedict = {"aa":1,"c":[{"a":2,"c":"vvvff"}]}
    casedict = {
                    'testcases': [{
                        'interfaceName': '/operation-manage/product/add',
                        'case': [{
                            'testPoint': '新增一个活动正常',
                            'preConditions': ['tearDBdel_t_content_picture_byTitle', 'tearDBdel_t_sku_byTitle', 'tearDBdel_t_vendor_rel_byTitle', 'tearDBdel_t_tag_rel_byTitle', 'tearDBdel_t_resource_byTitle'],
                            'operationSteps': 'addActivity',
                            'testData': [{
                                'resourceId': '',
                                'title': 'QUEENS PALACE高级定制馆1-自动化',
                                'subTitle': "QUEEN'S PALACE高级定制馆-活动副标题",
                                'deliverType': 0,
                                'vendorIdList': [3],
                                'resourceTypeId': 12,
                                'content': 'fQueen’s Palace于2011年9月创立，是一家国内高级定制婚纱礼服奢侈品牌。自品牌创立以来，Queen’s Palace在沪上高定婚纱品牌的殿堂一直雄踞顶端，专注于婚纱定制的每一处细节',
                                'shareType': 1,
                                'shareTitle': "QUEEN'S PALACE高级定制馆-分享标题",
                                'shareDescription': "QUEEN'S PALACE高级定制馆-分享描述",
                                'sharePicturePath': 'http://uat-steam.opg.cn/_static/admin/images/resource/20180507101830_796382.jpg',
                                'province': '重庆市',
                                'city': '重庆郊县',
                                'addressDetail': '肇嘉浜路356号(襄阳南路路口)',
                                'thumbUrl': 'http://uat-steam.opg.cn/_static/admin/images/resource/20180507101738_928360.jpg',
                                'bannerUrl': 'http://uat-steam.opg.cn/_static/admin/images/resource/20180507101741_710087.jpg',
                                'imgListpicturePath1': 'http://uat-steam.opg.cn/_static/admin/images/resource/20180507101747_909470.jpg',
                                'imgListpicturePath2': 'http://uat-steam.opg.cn/_static/admin/images/resource/20180507101749_880315.jpg',
                                'cornerMask': '商品',
                                'offShelfTime': 2764800000,
                                'entryIdList': [7],
                                'tagIdList': [2],
                                'skuName1': '套餐1',
                                'skuId1': None,
                                'order1': 1,
                                'price1': '0.01',
                                'originPrice1': '1000',
                                'inventory1': '1000',
                                'limitCount1': '2',
                                'postPrice1': '0.01',
                                'skuName2': '套餐2',
                                'skuId2': None,
                                'order2': 2,
                                'price2': '0.02',
                                'originPrice2': '1200',
                                'inventory2': '2000',
                                'limitCount2': '3',
                                'postPrice2': '0.01',
                                'state': 1,
                                'caseid': 'activity_add_1',
                                'testPoint': '/operation-manage/product/add'
                            }],
                            'expectedResult': [{
                                'code': '000000'
                            }]
                        }, {
                            'testPoint': '新增一个商品正常',
                            'preConditions': ['tearDBdel_t_content_picture_byTitle', 'tearDBdel_t_sku_byTitle', 'tearDBdel_t_vendor_rel_byTitle', 'tearDBdel_t_tag_rel_byTitle', 'tearDBdel_t_resource_byTitle'],
                            'operationSteps': 'addActivity',
                            'testData': [{
                                'resourceId': '',
                                'title': 'QUEENS PALACE高级定制馆1-自动化',
                                'subTitle': "QUEEN'S PALACE高级定制馆-活动副标题",
                                'deliverType': 0,
                                'vendorIdList': [3],
                                'resourceTypeId': 11,
                                'content': 'fQueen’s Palace于2011年9月创立，是一家国内高级定制婚纱礼服奢侈品牌。自品牌创立以来，Queen’s Palace在沪上高定婚纱品牌的殿堂一直雄踞顶端，专注于婚纱定制的每一处细节',
                                'shareType': 1,
                                'shareTitle': 'QUEENSPALACE高级定制馆-分享标题',
                                'shareDescription': "QUEEN'S PALACE高级定制馆-分享描述",
                                'sharePicturePath': 'http://uat-steam.opg.cn/_static/admin/images/resource/20180507101830_796382.jpg',
                                'province': '重庆市',
                                'city': '重庆郊县',
                                'addressDetail': '肇嘉浜路356号(襄阳南路路口)',
                                'thumbUrl': 'http://uat-steam.opg.cn/_static/admin/images/resource/20180507101738_928360.jpg',
                                'bannerUrl': 'http://uat-steam.opg.cn/_static/admin/images/resource/20180507101741_710087.jpg',
                                'imgListpicturePath1': 'http://uat-steam.opg.cn/_static/admin/images/resource/20180507101747_909470.jpg',
                                'imgListpicturePath2': 'http://uat-steam.opg.cn/_static/admin/images/resource/20180507101749_880315.jpg',
                                'cornerMask': '商品',
                                'offShelfTime': 2764800000,
                                'entryIdList': [7],
                                'tagIdList': [2],
                                'skuName1': '套餐1',
                                'skuId1': None,
                                'order1': 1,
                                'price1': '0.01',
                                'originPrice1': '1000',
                                'inventory1': '1000',
                                'limitCount1': '2',
                                'postPrice1': '0.01',
                                'skuName2': '套餐2',
                                'skuId2': None,
                                'order2': 2,
                                'price2': '0.02',
                                'originPrice2': '1200',
                                'inventory2': '2000',
                                'limitCount2': '3',
                                'postPrice2': '0.01',
                                'state': 1,
                                'caseid': 'goods_add_1',
                                'testPoint': '/operation-manage/product/add'
                            }],
                            'expectedResult': [{
                                'code': '000000'
                            }]
                        }]
                    }]
                }
    dumpDataToYmlFile(filePath="D:\\litaojun\\steamyml\\testa.yml",data=casedict)
    #tranXlsToYmlFile(casedict = casedict)\
    print("fsdf.yml".endswith(".yml"))