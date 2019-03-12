#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback


class Connection(object):
    def __init__(self, conn, connected_time):
        self.conn = conn
        self.connected_time = connected_time
        self.has_error = False

    def close(self):
        self.conn.close()

    def execute(self, query, args=None):
        result = None
        try:
            with self.conn.cursor() as cursor:
                n = cursor.execute(query, args)
                result = (n, cursor.lastrowid)
        except:
            err = traceback.format_exc().replace('\n', ' ')
            print( 'db error: %s, query: %s, args: %s' % (err, query, args))
            self.has_error = True
        return result

    def query(self, query, args=None):
        result = None
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, args)
                result = cursor.fetchall()
        except:
            self.has_error = True
        return result

    def query_one(self, query, args):
        result = None
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, args)
                result = cursor.fetchone()
        except:
            self.has_error = True
        if not self.has_error and result is None:
            result = {}
        return result
