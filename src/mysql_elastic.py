#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author : Alenx.Hai <alenx.hai@gmail.com>
# created time: 2020/12/29-11:15 上午
import os
import pymysql
import json
from elasticsearch import helpers
from elasticsearch.helpers import BulkIndexError
from common import row_handlers
from common.ConnectHelper import ConnectHelper
from common.extend_json_encoder import ExtendJSONEncoderFTime
from common.utils import timer


class MySQLElasticSearch(ConnectHelper):
    def __init__(self):
        self.custom_rowhandlers = None
        self.docs = []
        self.__instance = ConnectHelper()
        self.cur = pymysql.cursors.SSDictCursor
        self.sql_path = (os.path.abspath(os.path.join(
                os.path.dirname(__file__), "..")) + '/properties/{}')

    def get_mysql_data(self):
        __cur__ = self.__instance.mysql_conn().cursor(cursor=self.cur)
        try:
            if self.sql_statement.endswith('.sql'):
                try:
                    with open(self.sql_path.format(self.sql_statement), encoding='utf-8', mode='r') as f:
                        __cur__.execute(f.read())
                        return __cur__.fetchall()
                except FileExistsError as e:
                    self.logger.error('not fount sql files!')
            else:
                if isinstance(self.sql_statement, str):
                    __cur__.execute(self.sql_statement)
                    return __cur__.fetchall()
        except FileExistsError as e:
            self.logger.error("Please check the parameter sql_statement error!")

        finally:
            __cur__.close()
            self.__instance.mysql_conn().close()

    def do_pipeline(self, pipeline, row):
        if isinstance(row, dict):
            row = [row]

        # row 可能是个列表或迭代器
        for line in pipeline:
            row_ = []
            for r in row:
                func_name, kwargs = line.items()[0]
                func = getattr(self.custom_rowhandlers, func_name, None) or getattr(row_handlers, func_name)
                r_new = func(r, **kwargs)
                if isinstance(r_new, dict):
                    row_.append(r_new)
                else:
                    row_.extend(list(r_new))
            row = row_
        rows = row
        return rows

    def upload_docs(self):
        try:
            helpers.bulk(self._es_conn, self.docs)
        except BulkIndexError as e:
            self.logger.error("elasticsearch bulk errors !")

    @timer
    def put_data(self):
        if not self.get_mysql_data():
            return False
        for data_list in self.get_mysql_data():
            data = json.dumps(data_list, cls=ExtendJSONEncoderFTime)
            jsondata = json.loads(data)
            action = {
                "_id": jsondata['{}'.format(self.doc_id)],
                "_type": "_doc",
                "_index": '{}'.format(self.index_name),
                "_source": data
            }
            self.docs.append(action)
            if len(self.docs) >= self.bulk_size:
                self.upload_docs()

        self.upload_docs()