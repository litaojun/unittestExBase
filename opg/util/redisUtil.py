#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2018年1月9日 上午11:20:23
@author: li.taojun
'''
import redis

class RedisOper(object):
    '''
       xml 文件解析
    '''
    sign = True
    curRedis = None
    def __init__(self,host = "uop-uat-common.jl93bm.ng.0001.cnn1.cache.amazonaws.com.cn",port = 6379):
        '''
               host ： 要解析xml文 件路径
               port: 端口
               
        '''
        RedisOper.iniRedis(host, port)
    
    @staticmethod
    def iniRedis(host,port):
        if RedisOper.sign :
            RedisOper.curRedis  = redis.Redis(host,port)
            RedisOper.sign = False
        
    @staticmethod
    def getRedis(host,port):
        RedisOper.iniRedis(host,port)
        return RedisOper.curRedis  
        
    def keys(self,key = ""):
        cmredis = RedisOper.curRedis
        keyls = cmredis.keys(pattern=key)
        return keyls
        
    def getValue(self,key = ""):
        cvalue = RedisOper.curRedis.get(key)
        return cvalue
        
if __name__ == '__main__':
    redisOper = RedisOper()
    cvalue = redisOper.getValue("uop-x-sms:sendNum:18516099506")
    print(type(cvalue),cvalue)
    keyls = redisOper.keys("uop-x-sms:verifyCode:18516099506*")
    print(type(keyls),keyls)