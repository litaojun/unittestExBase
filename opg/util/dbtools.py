import pymysql
import time
import os
from DBUtils.PooledDB import PooledDB
import configparser
config_path = os.path.join(os.getcwd(), 'config', 'dbConfig.ini')
config = configparser.ConfigParser()  # 调用配置文件读取
config.read(config_path, encoding='utf-8')


class ReadConfig():
    def get_mysql(self, base, name):
        value = config.get(base, name)  # 通过config.get拿到配置文件中DATABASE的name的对应值
        return value


def printSql(func):
    def _fun(*args, **kwargs):
        for key in kwargs:
            if key.startswith("sql"):
                print("key = %s,sql = %s" % (key, kwargs[key]))
                break
        return func(*args, **kwargs)
    return _fun


class DbManager():
    connList = []
    sign = True
    conn = None

    def __init__(self,
                 host="192.168.0.103",
                 user="root",
                 password="123456",
                 dbname="test",
                 port=3306):
        DbManager.cleanDB()
        DbManager.initConn(host, user, password, dbname, port)
        self.conn = DbManager.getDbManager()

    @staticmethod
    def initConn(host, user, password, dbname, port):
        if DbManager.sign:
            DbManager.conn = pymysql.connect(host,
                                             user,
                                             password,
                                             dbname,
                                             port,
                                             use_unicode=True,
                                             charset="utf8",
                                             connect_timeout=100,
                                             write_timeout=100)
            DbManager.connList.append(DbManager.conn)
            DbManager.sign = False

    @staticmethod
    def cleanDB():
        # if not DbManager.sign :
        #     DbManager.connList.append(DbManager.conn)
        DbManager.sign = True
        DbManager.conn = None

    @staticmethod
    def closeDbConn():
        for conn in DbManager.connList:
            conn.close()

    def queryAll(self, sql, param=None):
        results = None
        try:
            cur = self.conn.cursor()
            cur.execute(sql)  # 执行sql语句
            results = cur.fetchall()  # 获取查询的所有记录
            self.conn.commit()
        except Exception as e:
            raise e
        finally:
            # self.conn.close()  #关闭连接
            return results
    # @printSql

    def insertData(self, sql_insert=""):
        num = 0
        cur = self.conn.cursor()
        #sql_insert ="""insert into user(id,username,password) values(4,'liu','1234')"""

        try:
            cur.execute(sql_insert)
            # 提交
            self.conn.commit()
            num = cur.rowcount
        except Exception as e:
            print(e)
            # 错误回滚
            self.conn.rollback()
            raise e
        finally:
            pass
            # self.conn.close()
        return num

    def deleteData(self, sql_del):
        num = 0
        try:
            cur = self.conn.cursor()
            cur.execute(sql_del)  # 像sql语句传递参数
            # 提交
            self.conn.commit()
            num = cur.rowcount
        except Exception as e:
            # 错误回滚
            num = 0
            self.conn.rollback()
        finally:
            # self.conn.close()
            pass
        return num

    def updateData(self, sql_update):
        try:
            cur = self.conn.cursor()
            cur.execute(sql_update)  # 像sql语句传递参数
            self.conn.commit()  # 提交
        except Exception as e:
            # 错误回滚
            self.conn.rollback()
        finally:
            # self.conn.close()
            time.sleep(1)

    @staticmethod
    def getDbManager():
        return DbManager.conn

    @staticmethod
    def a(self):
        sqlinsert = 'insert into test ( channel, subject, content, message_type) VALUES (3,4,5,6)'
        sqldel = 'delete t.* from test t where t.mid=%d'
        sqlquery = 'select * from test;'
        dbtest = DbManager()
        dbtest.insertData(sql_insert=sqlinsert)
        dbtest.deleteData(sql_del=sqldel % 1)
        res = dbtest.queryAll(sql=sqlquery)
        print(res)


class Database:
    sign = True
    dbDict = {}

    def __init__(self):
        print("Database.sign = %s" % str(Database.sign))
        if Database.sign:
            # self.dbDict = {}
            Database._CreatePool()
            Database.sign = False

    @classmethod
    def _CreatePool(self):
        for dbName in config.sections():
            print("init PooledDB()")
            Database.dbDict[dbName] = PooledDB(
                creator=pymysql,
                mincached=2,
                maxcached=5,
                maxshared=3,
                maxconnections=6,
                blocking=True,
                host=config.get(
                    dbName,
                    "host"),
                port=int(
                    config.get(
                        dbName,
                        "port")),
                user=config.get(
                    dbName,
                    "user"),
                password=config.get(
                    dbName,
                    "password"),
                database=config.get(
                    dbName,
                    "database"),
                charset="utf8")

    def _Getconnect(self, dbName):
        self.conn = Database.dbDict[dbName].connection()
        cur = self.conn.cursor()
        if not cur:
            raise("数据库连接不上")
        else:
            return cur
    # 查询sql

    def ExecQuery(self, sql):
        cur = self._Getconnect()
        cur.execute(sql)
        relist = cur.fetchall()
        cur.close()
        self.conn.close()
        return relist
    # 非查询的sql

    def ExecNoQuery(self, sql):
        cur = self._Getconnect()
        cur.execute(sql)
        self.conn.commit()
        cur.close()
        self.conn.close()

    def insertData(self, sql="", dbName=""):
        num = 0
        cur = self._Getconnect(dbName)
        # sql_insert ="""insert into user(id,username,password) values(4,'liu','1234')"""
        try:
            cur.execute(sql)
            # 提交
            self.conn.commit()
            num = cur.rowcount
        except Exception as e:
            print(e)
            # 错误回滚
            self.conn.rollback()
            raise e
        finally:
            cur.close()
            self.conn.close()
        return num

    def deleteData(self, sql="", dbName=""):
        num = 0
        cur = self._Getconnect(dbName)
        try:
            cur.execute(sql)  # 像sql语句传递参数
            # 提交
            self.conn.commit()
            num = cur.rowcount
        except Exception as e:
            # 错误回滚
            num = 0
            self.conn.rollback()
        finally:
            cur.close()
            self.conn.close()
        return num

    def updateData(self, sql="", dbName=""):
        cur = self._Getconnect(dbName)
        try:
            cur.execute(sql)  # 像sql语句传递参数
            self.conn.commit()  # 提交
        except Exception as e:
            # 错误回滚
            self.conn.rollback()
        finally:
            cur.close()
            self.conn.close()

    def queryAll(self, sql, dbName=""):
        results = None
        cur = self._Getconnect(dbName)
        try:
            # cur =self.conn.cursor()
            cur.execute(sql)  # 执行sql语句
            results = cur.fetchall()  # 获取查询的所有记录
            self.conn.commit()
        except Exception as e:
            raise e
        finally:
            cur.close()
            self.conn.close()
            return results


if __name__ == '__main__':
    sqlstr = "delete o.* from tb_order o where o.id = '11111fffffff'"
    db = Database()
    num = db.deleteData(sql=sqlstr, dbName="allin")
    print(str(num))
