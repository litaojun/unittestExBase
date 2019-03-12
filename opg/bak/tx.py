#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Transaction(object):
    def __init__(self, pool, conn):
        self.conn = conn
        self.pool = pool

    def _close(self):
        self.pool.put_conn(self.conn)
        self.pool = self.conn = None

    def execute(self, query, args):
        return self.conn.execute(query, args)

    def query(self, query, args):
        return self.conn.query(query, args)

    def query_one(self, query, args):
        return self.conn.query_one(query, args)

    def commit(self):
        self.conn.conn.commit()
        self._close()

    def rollback(self):
        self.conn.conn.rollback()
        self._close()

    def __del__(self):
        if self.pool:
            self.pool.close_conn(self.conn)