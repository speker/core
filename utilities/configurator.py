# -*- coding: utf-8 -*-

import os
import json
from core.helpers.crypt import Crypt


class Configuration:

    @staticmethod
    def get_configuration():

        path = os.path.dirname(os.path.abspath(__file__)) + "/../../conf/conf.json"
        json_data = json.loads(open(path).read())
        debug = json_data['debug']
        app_name = json_data['app_name']
        __dict__ = json_data[json_data['env']]
        __dict__['debug'] = debug
        __dict__['app_name'] = app_name

        crypt = Crypt

        try:
            __dict__['system']['tcp_server']['pg_sql']['user'] = \
                crypt(__dict__['system']['tcp_server']['pg_sql']['user']).decrypt()
            __dict__['system']['tcp_server']['pg_sql']['password'] = \
                crypt(__dict__['system']['tcp_server']['pg_sql']['password']).decrypt()
            __dict__['system']['tcp_server']['my_sql']['user'] = \
                crypt(__dict__['system']['tcp_server']['my_sql']['user']).decrypt()
            __dict__['system']['tcp_server']['my_sql']['password'] = \
                crypt(__dict__['system']['tcp_server']['my_sql']['password']).decrypt()
            __dict__['system']['tcp_server']['ms_sql']['user'] = \
                crypt(__dict__['system']['tcp_server']['ms_sql']['user']).decrypt()
            __dict__['system']['tcp_server']['ms_sql']['password'] = \
                crypt(__dict__['system']['tcp_server']['ms_sql']['password']).decrypt()
            __dict__['system']['tcp_server']['redis']['redis_auth'] = \
                crypt(__dict__['system']['tcp_server']['redis']['redis_auth']).decrypt()
            __dict__['system']['rest_server']['redis']['redis_auth'] = \
                crypt(__dict__['system']['rest_server']['redis']['redis_auth']).decrypt()

        except Exception as ecx:
            print(ecx)

        return __dict__
