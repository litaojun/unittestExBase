#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017

@author: li.taojun
'''
import time
from datetime import datetime
from datetime import timedelta


def strStrptime(
        timeStr="2016-05-05 20:28:54",
        dateFormate="%Y-%m-%d %H:%M:%S"):
    # 转换成时间数组
    timeArray = time.strptime(timeStr, dateFormate)
    return timeArray

# 将时间转换成时间戳


def strStrpTimestamp(
        timeStr="2016-05-05 20:28:54",
        dateFormate="%Y-%m-%d %H:%M:%S"):
    timearray = strStrptime(timeStr, dateFormate)
    timestamp = time.mktime(timearray)
    return timestamp


def strRepeatStrftime(
        timeStr="2016-05-05 20:28:54",
        fromdateFormate="%Y-%m-%d %H:%M:%S",
        todataformate="%Y%m%d-%H:%M:%S"):
    # 转换成时间数组
    timeArray = time.strptime(timeStr, "%Y-%m-%d %H:%M:%S")
    # 转换成新的时间格式(20160505-20:28:54)
    dt_new = time.strftime("%Y%m%d-%H:%M:%S", timeArray)
    return dt_new

# 将时间戳转换成时间


def timestampFtime(timestamp=1462451334, formatdate="%Y-%m-%d %H:%M:%S"):
    # 转换成localtime
    time_local = time.localtime(timestamp)
    # 转换成新的时间格式(2016-05-05 20:28:54)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt

# 按指定的格式获取当前时间


def getNowTime(formatedate="%Y-%m-%d %H:%M:%S"):
    # 获取当前时间,转换为时间戳
    time_now = int(time.time())
    print(time_now)
    # 转换成localtime
    time_local = time.localtime(time_now)
    # print(time_local)
    # 转换成新的时间格式(2016-05-09 18:59:20)
    dt = time.strftime(formatedate, time_local)
    # print(dt)
    return dt


def getYesterday(formatedate="%Y-%m-%d", delta=-1):
    '''
                      获取昨天的日期按制定格式返回
    '''
    now = datetime.now()
    aDay = timedelta(days=delta)
    now = now + aDay
    # print(now.strftime(formatedate))
    return now.strftime(formatedate)


def getNowday(formatedate="%Y-%m-%d"):
    '''
                      获取昨天的日期按制定格式返回
    '''
    now = datetime.now()
    print(now.strftime(formatedate))
    return now.strftime(formatedate)


def getNowTimeInt():
    time_now = int(time.time())
    return time_now


def getTimeIntByInPut(num=1):
    timestamp = getNowTimeInt()
    inputNum = num * 24 * 60 * 60
    return (timestamp + inputNum) * 1000


if __name__ == '__main__':
    timestamp = getNowday()
    print(timestamp)
    time_now = int(time.time())
    print(time_now)
    print(time_now * 1000)
    print(time_now + 24 * 60 * 60)
    print(getTimeIntByInPut(1))
    print(time_now - 24 * 60 * 60)
    print(getTimeIntByInPut(-1))
