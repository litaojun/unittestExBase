#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年7月9日

@author: ｌｉｔａｏｊｕｎ
'''
import os
from dynload import Dynload
from fileOper import walk_absdir_modul_file
from isSystemType import splict

#===============================================================================
# getModul
# path  相对当前目录
# sign  模块py文件标识，即py文件名包含"load"字符
# desc  获取相对目录下模块py文件名包含"load"字符的所有文件
# return 返回相对path路径下py文件名包含"load"字符的所有模块
# <module 'com.tao.opg.util.dynload' from 'D:\litaojun\workspace\a\unittestExtend\com\tao\opg\util\dynload.pyc'>]
#===============================================================================
s = splict
print "s=",s
def getModul(path='../../../',sign="load"):
    #定义lambda函数，将com\\bestv\\kafka\\kafkacon转换为(.com.bestv.kafka,.kafkacon)
    lfunc = lambda  x : os.path.splitext(os.path.basename(x.replace(s,"."))) 
    mfunc = lambda  x : x.replace(s,".")
    #定义lambda函数，将(x="com.bestv.kafka.kafkacon",y=[com.bestv.kafka,])加载为模块
    nfunc = lambda  x,y : Dynload(x,imp_list=y).getobject()
    print os.getcwd()
    #通过相对路径获取绝对路径
    curpath =  os.path.abspath(path)
    #加载绝对路径下的所有模块文件，格式["com\\bestv\\kafka\\kafkacon",]
    lsn = walk_absdir_modul_file(curpath,sign=sign,endstr=".py")
    a = map(lfunc,lsn)
    #将(.com.bestv.kafka,.kafkacon)转换为(com.bestv.kafka.kafkacon,com.bestv.kafka)
    d = tuple([(x[1:]+y,[x[1:]]) for x,y in a])
    #将(com.bestv.kafka.kafkacon,com.bestv.kafka)转换为模块
    mdlist = map(nfunc,[a[0] for a in d],[a[1] for a in d])
    return mdlist
#===============================================================================
# getModul
# path  绝对路径
# sign  模块py文件标识，即py文件名包含"load"字符
# desc  获取相对目录下模块py文件名包含"load"字符的所有文件
# return 返回相对path路径下py文件名包含"load"字符的所有模块
# <module 'com.tao.opg.util.dynload' from 'D:\litaojun\workspace\a\unittestExtend\com\tao\opg\util\dynload.pyc'>]
#===============================================================================
def getModulByabspath(path='',sign="load"):
    #定义lambda函数，将com\\bestv\\kafka\\kafkacon转换为(.com.bestv.kafka,.kafkacon)
    lfunc = lambda  x : os.path.splitext(os.path.basename(x.replace(s,"."))) 
    mfunc = lambda  x : x.replace(s,".")
    #定义lambda函数，将(x="com.bestv.kafka.kafkacon",y=[com.bestv.kafka,])加载为模块
    nfunc = lambda  x,y : Dynload(x,imp_list=y).getobject()
    print os.getcwd()
    #通过相对路径获取绝对路径
    #curpath =  os.path.abspath(path)
    curpath = path
    #加载绝对路径下的所有模块文件，格式["com\\bestv\\kafka\\kafkacon",]
    lsn = walk_absdir_modul_file(curpath,sign=sign,endstr=".py")
    a = map(lfunc,lsn)
    print "lsn=",lsn
    #将(.com.bestv.kafka,.kafkacon)转换为(com.bestv.kafka.kafkacon,com.bestv.kafka)
    d = tuple([(x[1:]+y,[x[1:]]) for x,y in a])
    #将(com.bestv.kafka.kafkacon,com.bestv.kafka)转换为模块
    mdlist = map(nfunc,[a[0] for a in d],[a[1] for a in d])
    return mdlist 
    
    
if __name__ == '__main__':
    moduls = getModul(path='../../../../',sign="ara")
    print moduls