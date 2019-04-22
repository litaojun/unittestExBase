#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017
@author: li.taojun
'''
import sys
# sys.path.append('D:\litaojun\workspace\jenkinsPython')


class Dynload():
    '''
    '''
    # =============================================================================
    # __init__
    # 调用格式(package="com.bestv.aws.ec2.ec2info",imp_list=['com.bestv.aws.ec2',])
    # =============================================================================

    def __init__(self, package, imp_list):
        self.package = package
        self.imp = imp_list

    # =============================================================================
    # getobject
    # desc 根据package,imp加载模块
    # self.package = "com.bestv.aws.ec2.ec2info"
    # self.imp = ['com.bestv.aws.ec2',]
    # =============================================================================
    @property
    def getobject(self):
        # print sys.path
        return __import__(self.package, globals(), locals(), self.imp)

    def getClassInstance(self, classstr, *args):
        return getattr(self.getobject, classstr)(*args)

    def execfunc(self, method, *args):
        return getattr(self.getobject, method)(*args)

    def execMegetattrthod(self, instance, method, *args):
        return (instance, method)(*args)


def tef():
    pass


if __name__ == '__main__':
    pass
#     dyn=Dynload("com.bestv.aws.ec2.ec2info",imp_list=['com.bestv.aws.ec2',])
#     a = dyn.getobject()
#     print(a,dir(a))
