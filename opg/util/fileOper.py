#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年7月8日

@author: ｌｉｔａｏｊｕｎ
'''
import os

from .isSystemType import splict
s = splict
# print("s=",s)
#===============================================================================
#dir  搜索目录
#sign 文件标识，文件名包含sign
#endstr 文件扩展名
#desc 搜索dir目录下文件名包含case字样，且扩展名为.csv的所有用例文件
#return 
#['D:\\litaojun\\workspace\\a\\unittestExtend\\testcase\\admin\\baoming\\testcase-baoming.csv',
# 'D:\\litaojun\\workspace\\a\\unittestExtend\\testcase\\admin\\shangpin\\testcase-shangpin.csv' ]
# 
#===============================================================================
def walk_dir_test(dir,topdown=True,sign='case',endstr='.xlsx'):
    modelnm = []
    ts = os.walk(dir, topdown)
    for root, dirs, files in ts:
        #root = root.replace(dir,"")
        for name in files:
          if name.find(sign)>0 and name.endswith(endstr) > 0 :
              modelnm.append(root+s+name)
    return modelnm


#===============================================================================
# walk_absdir_modul_file
#dir 模块所在的绝对目录
#sign  加载模块文件标识，即模块文件名包含'con'字符
#endstr   加载模块文件标识，即模块文件后缀名为'.py'
#desc  加载绝对路径dir目录下，文件名包含'con'字符，后缀名为'.py'的所有模块文件
#return list数据，所有模块文件.py的绝对路径，如：['com\\bestv\\kafka\\kafkacon', 'com\\bestv\\kafka\\kafkaconSubscr', 'com\\bestv\\kafka\\kafkaconsume']
#===============================================================================
def walk_absdir_modul_file(dir,topdown=True,sign='con',endstr='.py'):
    modelnm = []
    ts = os.walk(dir, topdown)
    for root, dirs, files in ts:
        root = root.replace(dir,"")
        for name in files:
          if name.find(sign)>0 and name.endswith(endstr) > 0 :
              modelnm.append(root+s+name.replace(endstr,""))
    return modelnm


if __name__ == '__main__':
    # cspath = walk_dir_test("D:\\litaojun\\workspace\\a\\unittestExtend\\testcase")
    # print(cspath)
    # mouduls = walk_absdir_modul_file(dir='D:\\litaojun\\workspace\\jenkinsPython\\')
    # print(mouduls)
    a = walk_dir_test(dir=os.getcwd(),str="",endstr=".txt")
    print(str(a))