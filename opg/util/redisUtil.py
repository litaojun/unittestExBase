#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2018年1月9日 上午11:20:23
@author: li.taojun
'''
import redis


class RedisOper(object):
    '''
       reids
    '''
    sign = True
    curRedis = None

    def __init__(
            self,
            host="steam-uat-default.s4kcls.ng.0001.cnw1.cache.amazonaws.com.cn",
            port=6379):
        '''
               host ： ip地址
               port: 端口

        '''
        RedisOper.iniRedis(host, port)

    @staticmethod
    def iniRedis(host, port):
        if RedisOper.sign:
            RedisOper.curRedis = redis.Redis(host, port)
            RedisOper.sign = False

    @staticmethod
    def getRedis(host, port):
        RedisOper.iniRedis(host, port)
        return RedisOper.curRedis

    def keys(self, key=""):
        cmredis = RedisOper.curRedis
        keyls = cmredis.keys(pattern=key)
        return keyls

    def getValue(self, key=""):
        cvalue = RedisOper.curRedis.get(key)
        return cvalue

    def getSteamVerCodeByPhone(self, phone='18916899938', scenes="QTP"):
        # PASSPORT_VERIFY_CODE:MLN:18516099509_235934
        vercodeDict = {
            "OTP": "PASSPORT_VERIFY_CODE:OTP:%s%s",
            "MP": "PASSPORT_VERIFY_CODE:MLN:%s%s",
            "MER": "steam-merchant:SMS:%s_%s"
        }
        keycodefmt = vercodeDict[scenes] % (phone, "*")
        keyls = RedisOper.curRedis.keys(keycodefmt)
        code = b'ss'
        if len(keyls) > 0:
            key = keyls[0]
            code = key[-6:]
            print(type(code))
        return str(code, encoding="utf-8")

    def getTokenDataList(self, formatStr="STEAM_PERMISSION:TOKEN:*"):
        tokenList = RedisOper.curRedis.keys(formatStr)
        tokenMbID = []
        for tokendata in tokenList:
            token = tokendata[23:]
            memberId = RedisOper.curRedis.get(token)
            tokenMbID.append((token, memberId))
        return tokenMbID


if __name__ == '__main__':
    pass
