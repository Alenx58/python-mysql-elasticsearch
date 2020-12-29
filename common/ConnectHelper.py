#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author : Alenx.Hai <alenx.hai@gmail.com>
# created time: 2020/12/17-7:28 下午

import pymysql
from elasticsearch import Elasticsearch, ElasticsearchException
from redis import Redis, ConnectionPool, RedisError
from common import Notice


class ConnectHelper(Notice):

    def __init__(self):
        pass

    def mysql_conn(self, *args):
        global __instance__
        try:
            __instance__ = pymysql.connect(
                host=Notice.mysql_host,
                port=Notice.mysql_port,
                user=Notice.mysql_username,
                passwd=Notice.mysql_password,
                db=Notice.mysql_db,
                charset='UTF8',
            )

            return __instance__
        except pymysql.MySQLError as e:
            self.logger.error("数据库链接异常请检查！", e)
            return False

    def _redis_conn(self):
        try:
            pool = ConnectionPool(
                host=Notice.redis_host,
                port=Notice.redis_port,
                password=Notice.redis_password,
                db=Notice.redis_db,
                encoding='utf-8',
                decode_responses=True)

            __redis = Redis(connection_pool=pool)
            return __redis
        except RedisError as e:
            self.logger.error("Redis 链接异常请检查！", e)
            return False

    @property
    def _es_conn(self, *args):
        try:
            __es__ = Elasticsearch(
                hosts=Notice.es_host,
                headers=Notice.headers,
                http_auth=('{}'.format(Notice.es_username), '{}'.format(Notice.es_password))
            )

            return __es__

        except ElasticsearchException as e:
            self.logger.error("Elasticsearch 链接异常请检查！", e)
            return False

    @property
    def doc_id(self):
        return Notice.doc_id

    @property
    def sql_statement(self):
        return Notice.sql_statement
