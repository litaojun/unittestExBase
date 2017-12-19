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
        num = 0
        cur = self.conn.cursor()  
        #sql_insert ="""insert into user(id,username,password) values(4,'liu','1234')"""  

        try:  
            cur.execute(sql_insert)  
            #提交  
            self.conn.commit()  
            num = cur.rowcount;
        except Exception as e:  
            print(e)
            #错误回滚  
            self.conn.rollback()
            raise e
        finally:  
            #self.conn.close()
            pass
        return num
    def deleteData(self,sql_del):
        num = 0
        try:  
            cur = self.conn.cursor() 
            cur.execute(sql_del)  #像sql语句传递参数  
            #提交  
            self.conn.commit()  
            num = cur.rowcount
        except Exception as e:  
                #错误回滚  
                self.conn.rollback()   
        finally:  
                #self.conn.close()
                pass 
        return num
                
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
    
    def initdata(self):
        stuls = [
                 "insert student(sname,sage,ssex) values('litaojun',31,1);",
                 "insert student(sname,sage,ssex) values('chenming',32,1);",
                 "insert student(sname,sage,ssex) values('youyou',30,1);",
                 "insert student(sname,sage,ssex) values('guohui',28,0);"
                ]      
        tidls = ["insert teacher(tname) values('zhongming');",
                 "insert teacher(tname) values('chennan');"]
        coursels = ["insert course(cname,tid) VALUES('yuwen',1);",
                    "insert course(cname,tid) VALUES('shuxue',2);",
                   ]
        scls = ["insert sc(sid,cid,score) values(1,1,80);",
                "insert sc(sid,cid,score) values(2,1,40);",
                "insert sc(sid,cid,score) values(3,1,69);",
                "insert sc(sid,cid,score) values(4,1,99);",
                "insert sc(sid,cid,score) values(1,2,79);",
                "insert sc(sid,cid,score) values(2,2,88);",
                "insert sc(sid,cid,score) values(3,2,67);",
                "insert sc(sid,cid,score) values(4,2,55);"]
        #dbtest = DbManager()
        f = lambda x : self.insertData(x)
        a = map(f,stuls)
        print(list(a))
        b = map(f,tidls)
        print(list(b))
        c = map(f,coursels)
        print(list(c))
        d = map(f,scls)
        print(list(d))
        
    @staticmethod
    def a(self):
        sqlinsert = 'insert into test ( channel, subject, content, message_type) VALUES (3,4,5,6)'
        sqldel = 'delete t.* from test t where t.mid=%d'
        sqlquery = 'select * from test;'
        dbtest = DbManager()
        dbtest.insertData(sql_insert = sqlinsert)
        dbtest.deleteData(sql_del= sqldel % 1)
        res = dbtest.queryAll(sql = sqlquery)
        print(res)
if __name__ == '__main__':
    sqlstr = "delete t.* from t_raffle_result_address t where EXISTS(select 1 from     t_raffle_result f where    t.RESULT_ID = f.id and f.MEMBER_ID = 'ab4d6667-e04c-447d-85a1-c78e9b3e42fe' and f.ACTIVITIES_ID ='1a1c0272-769a-44b1-9cc3-1b4163f537a5');"
    db = DbManager(host="uop-uat-wx.cmcutmukkzyn.rds.cn-north-1.amazonaws.com.cn",user="root",password="Bestv001!",dbname="ltjtest",port=3306)
    num = db.deleteData(sql_del = sqlstr)
    print(str(num))