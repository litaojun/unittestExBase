#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
import time
from opg.bak.connection import Connection
from opg.bak.tx import Transaction


class Pool(object):
    def __init__(self, conn_cfg, max_lifetime=3600, max_open=0):
        self.conn_cfg = conn_cfg
        self.max_lifetime = max_lifetime
        self.max_open = max_open
        self._free_conns = []

    def make_conn(self):
        conn = pymysql.connect(
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
            **self.conn_cfg
        )
        now = int(time.time())
        return Connection(conn, now)

    def get_conn(self):
        try:
            now = int(time.time())
            conn = self._free_conns.pop()
            if now - conn.connected_time > self.max_lifetime:
                self.close_conn(conn)
                conn = None
        except:
            conn = None
        if not conn:
            conn = self.make_conn()
        return conn

    def put_conn(self, conn):
        if conn.has_error or len(self._free_conns) > self.max_open:
            self.close_conn(conn)
        else:
            self._free_conns.append(conn)

    def close_conn(self, conn):
        conn.close()

    def execute(self, query, args=None):
        conn = self.get_conn()
        result = conn.execute(query, args)
        self.put_conn(conn)
        return result

    def query(self, query, args=None):
        conn = self.get_conn()
        result = conn.query(query, args)
        self.put_conn(conn)
        return result

    def query_one(self, query, args=None):
        conn = self.get_conn()
        result = conn.query_one(query, args)
        self.put_conn(conn)
        return result

    def begin(self):
        conn = self.get_conn()
        try:
            conn.conn.begin()
        except:
            conn.has_error = True
            self.put_conn(conn)
            return
        return Transaction(self, conn)

#     def insert(self):
#         conn = self.get_conn()
#         result = conn
        