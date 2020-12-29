#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author : Alenx.Hai <alenx.hai@gmail.com>
# created time: 2020/12/17-7:27 下午

import logging
import os
import yaml


class Notice(object):

        logger = logging.getLogger("simple")

        config = (os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) + '/properties/application.yaml')

        headers = {
            'Content-Type': 'application/json;charset=UTF-8'
        }

        if os.path.exists(config):
            with open(config, 'r', encoding='utf-8') as f:
                config = yaml.load(f, Loader=yaml.FullLoader)

        logger.info('connet: {}'.format(config))

        mysql_host = config['mysql']['host']
        mysql_port = config['mysql']['port']
        mysql_username = config['mysql']['username']
        mysql_password = config['mysql']['password']
        mysql_db = config['mysql']['db']
        sql_statement = config['mysql']['sql_statement']

        redis_host = config['redis']['host']
        redis_port = config['redis']['port']
        redis_password = config['redis']['password']
        redis_db = config['redis']['db']

        es_host: list = config['elasticsearch']['host']
        es_username = config['elasticsearch']['username']
        es_password = config['elasticsearch']['password']
        doc_id = config['elasticsearch']['id']
        index_name = config['elasticsearch']['index_name']
        bulk_size = config['elasticsearch']['bulk_size']
