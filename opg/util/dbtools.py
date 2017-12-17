#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年12月16日
http://blog.csdn.net/MemoryD/article/details/74995651
@author: ｌｉｔａｏｊｕｎ
'''
import pymysql 

class DbManager():
    def __init__(self,
                   host="192.168.0.103",
                   user="root",
                   password="123456",
                   dbname="test",
                   port=3306):
          self.conn= pymysql.connect(host,user,  password,dbname,port,connect_timeout=100,write_timeout=100)
    def queryAll(self,sql,param=None): 
          results = None 
          try:  
            cur =self.conn.cursor() 
            cur.execute(sql)    #执行sql语句  
            results = cur.fetchall()    #获取查询的所有记录  
#             print("id","name","password")  
#             #遍历结果   
#             for row in results :  
#                 id = row[0]  
#                 name = row[1]  
#                 password = row[2]  
#                 print(id,name,password)  
          except Exception as e:  
                raise e  
          finally:  
                #self.conn.close()  #关闭连接 
                return results
    
    def insertData(self,sql_insert):
        cur = self.conn.cursor()  
        #sql_insert ="""insert into user(id,username,password) values(4,'liu','1234')"""  

        try:  
            cur.execute(sql_insert)  
            #提交  
            self.conn.commit()  
        except Exception as e:  
            #错误回滚  
            self.conn.rollback()
            raise e
        finally:  
            #self.conn.close()
            pass
    
    def deleteData(self,sql_del):
        try:  
            cur = self.conn.cursor() 
            cur.execute(sql_del)  #像sql语句传递参数  
            #提交  
            self.conn.commit()  
        except Exception as e:  
                #错误回滚  
                self.conn.rollback()   
        finally:  
                #self.conn.close()
                pass 
                
    def updateData(self,sql_update):
        try:  
            cur = self.conn.cursor() 
            cur.execute(sql_update)  #像sql语句传递参数  
            #提交  
            self.conn.commit()  
        except Exception as e:  
                #错误回滚  
                self.conn.rollback()   
        finally:  
                #self.conn.close()
                pass 
if __name__ == '__main__':
    dbtest = DbManager()
    dbtest.insertData(sql_insert = 'insert into test (mid, channel, subject, content, message_type) VALUES (2,3,4,5,6)')
    res = dbtest.queryAll(sql = 'select * from test;')
    print(res)