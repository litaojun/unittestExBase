#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017��6��29��

@author: li.taojun
判断当前操作系统，目前主要判断windows,linux两种
'''
import platform
def TestPlatform():
    print ("----------Operation System--------------------------")
    #Windows will be : (32bit, WindowsPE)
    #Linux will be : (32bit, ELF)
    print(platform.architecture())

    #Windows will be : Windows-XP-5.1.2600-SP3 or Windows-post2008Server-6.1.7600
    #Linux will be : Linux-2.6.18-128.el5-i686-with-redhat-5.3-Final
    print(platform.platform())

    #Windows will be : Windows
    #Linux will be : Linux
    print(platform.system())

    print ("--------------Python Version-------------------------")
    #Windows and Linux will be : 3.1.1 or 3.1.3
    print(platform.python_version())

def UsePlatform():
  sysstr = platform.system()
  if(sysstr =="Windows"):
    print ("Call Windows tasks")
  elif(sysstr == "Linux"):
    print ("Call Linux tasks")
  else:
    print ("Other System tasks")
def getPlatfromType():
  sysstr = platform.system()
  retsystype = 1
  if(sysstr =="Windows"):
    retsystype = 1 
  elif(sysstr == "Linux"):
     retsystype = 2
  else:
     retsystype = 3
  return retsystype

def getfileopertr():
    splic = "\\"
    sign = getPlatfromType()
    if sign == 2:
        splic = "/"
    return splic
splict = getfileopertr()
if __name__ == '__main__':
    TestPlatform()
    UsePlatform()
    print getPlatfromType()