#!/usr/bin/env python
# -*- coding: utf-8 -*-


from opg.util.pools import Pool

mysql_pool = None

cfg = {
    'host': '192.168.0.103',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'test',
    'charset': 'utf-8',
    'autocommit': True,
}

def mysql_pool_connect(cfg):
    global mysql_pool
    mysql_pool = Pool(cfg, max_open=128)


if __name__ == "__main__":
    mysql_pool_connect(cfg)
    mysql_pool.execute('insert into test (mid, channel, subject, content, message_type) VALUES (2,3,4,5,6)')
    res = mysql_pool.query('select * from test;')
    print(res)
