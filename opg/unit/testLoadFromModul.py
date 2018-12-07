#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017

@author: li.taojun
'''
from opg.unit.parametrized import ParametrizedTestCase
from inspect import isfunction
#===============================================================================
# loadTestClassFromModule
# module <module 'com.tao.opg.util.dynload' from 'D:\litaojun\workspace\unittestExtend\com\tao\opg\util\dynload.pyc'>
# desc case.TestCase
# return 
#===============================================================================
def loadTestClassFromModule(module, use_load_tests=True):
    """Return a suite of all tests cases contained in the given module"""
    tests = None
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and issubclass(obj, ParametrizedTestCase) and str(obj) != str(ParametrizedTestCase) and str(obj) != "<class 'uopweixin.util.parametrizedCase.ParametrizedCase'>":
           if obj.__name__.endswith("Test"):
              tests = obj
    return tests
#===============================================================================
# 从模块中获取所有测试测试类（继承了ParametrizedTestCase）
# 
#===============================================================================
def loadTestClassFromModules(modules):
    testClass = []
    for mod in modules:
        tcls = loadTestClassFromModule(mod)
        if tcls is not None:
           testClass.append(tcls)
    return testClass

#===============================================================================
# 将测试类（继承了ParametrizedTestCase）转换为DICT，其中键值为对应的接口名称
#===============================================================================
def tranListClassToDict(testClass=[]):    
    func = lambda x:(x.__interfaceName__,x) if hasattr(x, "__interfaceName__")  else None
    tuplea = map(func,testClass)
    di = {}
    for t in tuplea:
        if t is not None:
          di[t[0]] = t[1]
    return di

def loadFunFromObject(obj = None):
     funls = []
     for name in dir(obj):
       objname = getattr(obj, name)
       if isfunction(objname) : 
         funls.append(objname)
     return funls
   
def filterFunByDecoratorName(funls = [],decoratorName = "__unittest_skip__"):
    decoratorls = []
    for fun in funls :
      if getattr(fun, decoratorName, False) is not None:
        decoratorls.append(fun)

if __name__ == '__main__':
      a = ParametrizedTestCase()
      print(type(a))
      print(type(ParametrizedTestCase))
      print(str(ParametrizedTestCase))