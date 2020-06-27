# -*- coding: utf-8 -*-

from core.reapy import ReaPy
from core.model import Model as LocalModel


class ReaMediation(object):
    __instance = None
    __db = None
    __count = 0
    __error = None
    __result = []
    __mediation_server = None
    coll = None
    __source_id = None
    __header = {'content-type': 'application/json'}
    _count_data = False 
    __get_count = 0

    def __init__(self):
        super(ReaMediation).__init__()
        if ReaMediation.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ReaMediation.__instance = self

    @staticmethod
    def get_instance(configurations, source_id):
        ReaMediation.__source_id = source_id

        if 'endpoint' in configurations:
            ReaMediation.__mediation_server = configurations['proto'] + '://' + configurations[
                'host'] + ':' + str(configurations['port']) + configurations['endpoint']

        else:
            ReaMediation.__mediation_server = configurations['proto'] + '://' + configurations[
                'host'] + ':' + str(configurations['port']) + '/source/db/connect'

        if ReaMediation.__instance is None:
            ReaMediation.__instance = ReaMediation()
        return ReaMediation.__instance

    def connect(self, payload):
        self.__count = 0
        self.__error = False
        self.__result = []
        self.coll = None
        request = ReaPy.requests().post(self.__mediation_server, data=ReaPy.json().dumps(payload),
                                        headers=self.__header)
        return request

    def select(self, table, field=None, condition=None, sort=None, top=None, cache=False, offset=None):
        data = None
        payload = {'method': 'select', 'source_id': self.__source_id, 'table': table, 'field': field,
                   'condition': condition, 'sort': sort, 'top': top,'offset': offset}
        if cache is True:
            hash_payload = ReaPy.hash().md5(ReaPy.json().dumps(payload))
            cache = self.get_cache(hash_payload)
            if cache is not None:
                cache_data = cache[0][1]
                data_json = ReaPy.json().loads(cache_data)
                data = data_json['data']
            else:
                request = self.connect(payload)
                if request is not None:
                    if request.status_code == 200:
                        data = request.json()['data']
                        self.set_cache(hash_payload, data)

        else:
            request = self.connect(payload)
            if request is not None:
                if request.status_code == 200:
                    data = request.json()['data']

        if data is not None:
            self.__count = data['count']
            self.__result = data['result']
            self.__error = data['error']
        return self

    def insert(self, table, condition):
        payload = {'method': 'insert', 'source_id': self.__source_id, 'table': table,
                   'condition': condition}

        request = self.connect(payload)
        data = request.json()['data']
        if request.status_code == 200:
            self.__count = data['count']
            self.__result = data['result']
            self.__error = data['error']
        return self

    def update(self, table, condition):
        payload = {'method': 'update', 'source_id': self.__source_id, 'table': table,
                   'condition': condition}

        request = self.connect(payload)
        data = request.json()['data']
        if request.status_code == 200:
            self.__count = data['count']
            self.__result = data['result']
            self.__error = data['error']
        return self

    def delete(self, table, condition):
        payload = {'method': 'delete', 'source_id': self.__source_id, 'table': table,
                   'condition': condition}

        request = self.connect(payload)
        data = request.json()['data']
        if request.status_code == 200:
            self.__count = data['count']
            self.__result = data['result']
            self.__error = data['error']
        return self


    def count(self):
        return self.__count

    def error(self):
        return self.__error

    def result(self):
        return self.__result

    def first(self):
        return [self.__result[0]]

    def count_data(self):
        self._count_data = True
        return self.__get_count

    @staticmethod
    def get_cache(cache_hash):
        data = LocalModel('ReaRedis').select(10, None, {
            0: {'col': 'Mediation_Model_Cache',
                'operator': '=', 'value': cache_hash}}).data()

        return data

    @staticmethod
    def set_cache(cache_hash, data):
        insert_cache = LocalModel('ReaRedis').insert(10, {
            0: {'Mediation_Model_Cache:' + cache_hash: {'data': data, }}}).data()
        return insert_cache
