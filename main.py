#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author : Alenx.Hai <alenx.hai@gmail.com>
# created time: 2020/12/21-10:49 上午
import asyncio
from src.mysql_elastic import MySQLElasticSearch


@asyncio.coroutine
def main():
    elastic = MySQLElasticSearch()
    yield elastic.put_data()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait([main()]))

