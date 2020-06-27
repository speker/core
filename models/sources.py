# -*- coding: utf-8 -*-
from core.drivers.rea_pgsql import ReaPgsql
from core.reapy import ReaPy


class Sources:
    cache_db = None

    def __init__(self):
        super(Sources).__init__()
        cache_configurations = ReaPy.configuration().get_configuration()['system']['tcp_server']['redis']
        self.cache_db = ReaPy.redis(host=cache_configurations['host'],
                                    port=cache_configurations['port'],
                                    db=13, password=cache_configurations['redis_auth'])

    @staticmethod
    def get_source(source_id):
        configurations = {}
        check_cache = Sources().get_cache(source_id)
        if check_cache is not None:
            configurations = ReaPy.json().loads(check_cache.decode('utf-8'))
        else:
            db = ReaPgsql.get_instance().select('public.get_source',
                                                None,
                                                {0: {'col': 'source_id', 'operator': '=', 'value': source_id}}
                                                ).first()
            configurations['driver'] = db[0][1]
            configurations['host'] = db[0][2]
            configurations['port'] = db[0][3]
            configurations['user'] = db[0][4]
            configurations['password'] = db[0][5]
            configurations['database'] = db[0][6]
            Sources().set_cache(source_id, configurations)
        return configurations

    def get_cache(self, cache_hash):
        cache = self.cache_db.get(cache_hash)
        return cache

    def set_cache(self, cache_hash, data):
        self.cache_db.set(cache_hash, ReaPy.json().dumps(data))
