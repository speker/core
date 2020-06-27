# -*- coding: utf-8 -*-

from core.reapy import ReaPy
from core.drivers import *
from core.models.sources import Sources
import math
import sys

class Model(object):
    _db = None
    _data = []
    _error = None
    _local_sources = {'ReaPgsql', 'ReaElastic', 'ReaKafka', 'ReaRedis', 'ReaMysql', 'ReaMssql'}
    _pagination = None
    pagination_offset = 0
    count_data = False
    _aktif_mi = None

    def __init__(self, source_id=None):
        if source_id is None:
            source = ReaPgsql
            configurations = None
        else:
            if source_id in self._local_sources:
                source = getattr(ReaPy.sys().modules[__name__], source_id)
                configurations = None
            else:
                configurations = Sources.get_source(source_id)
                source = getattr(ReaPy.sys().modules[__name__], configurations['driver'])
        self._db = source.get_instance(configurations)

    def data(self):
        try:
            if self._db.coll is not None:
                results = []
                if self._data is not None:
                    for row in self._data:
                        try:
                            results.append(dict(zip(self._db.coll, row)))
                        except Exception as e:
                            print(e)
                    if self.count_data:
                        count_data = self._db.count_data()
               
                        try:
                            sys.stdout.flush()
                            count_data = count_data[0]
                        except:
                            count_data = 0
                        total_page = math.ceil(int(count_data)/int(self.pagination_offset))
                        return results,count_data,total_page
                    else:
                        return results
                else:
                    if self.count_data:
                        return None,0,0
            else:
                return self._data
        except Exception as e:
            print(e)


    #pagination
    #params (top,offset) 
    #top=>total data
    #offset=>current page
    #basic example resource.pagination(top=10,offset=0).data()
    def pagination(self,offset=0, top=10):
        self._pagination = [offset,top]
        return self

    def count(self,pagination_offset):
        self.count_data = True
        self._db.count_data()
        self.pagination_offset = pagination_offset
        return self

    def aktif_mi(self,mi):
        self._aktif_mi = mi
        return self

    def error(self):
        return self._error

    def select(self, table, field=None, condition=None, sort=None, top=None, is_first=False, cache=False,
               offset=None):

        if self._pagination is not None:
            top = self._pagination[1]
            offset = self._pagination[0]

        try:
            cache_payload = {"table": table, 
                            "field": field, 
                            "condition": condition, 
                            "sort": sort, 
                            "top": top,
                            "offset": offset,
                            "is_first": is_first}

            #database aktif_mi add condition
            if self._aktif_mi is not None:
                if condition is None:
                    condition = []
                combiner_number = len(condition)
                if combiner_number>0:
                    condition[combiner_number-1]['combiner'] = 'AND'
                    condition[combiner_number] = {'col': 'aktif_mi', 'operator': '=', 'value': self._aktif_mi}
                else:
                    condition = {0:{'col': 'aktif_mi', 'operator': '=', 'value': self._aktif_mi}}
                
            if cache is True:
                hash_payload = ReaPy.hash().md5(ReaPy.json().dumps(cache_payload))
                
                cache = self.get_cache(hash_payload)
                sys.stdout.flush()
                if cache is not None:
                    try:
                        cache_data = cache[0][1]
                        data_json = ReaPy.json().loads(cache_data)
                        data = data_json['data']
                        count = data['count']
                        self._error = data['error']
                        self._db.coll = None
                        if count:
                            data_len = len(data['result'])
                            if data_len>0:
                                self._data = data['result']
                            else:
                                self._data = None
                        else:
                            self._data = None
                            try:
                                self._error = data.error()
                            except Exception as e:
                                print(e)
                        return self
                    except Exception as e:
                        print(e)

                else:
                    data = self._db.select(table, field, condition, sort, top, offset)
                    if data is None:
                        self._data = None
                        return self
                    if data.error()==False:
                        if is_first is True:
                            if data.count():
                                self._data = data.first()
                            else:
                                self._data = None
                        else: 
                            data_len = len(data.result())
                            sys.stdout.flush()
                            if data_len>0:
                                self._data = data.result()
                            else:
                                self._data = None
                            
                        cache_data = {"result": self.data(), "error": self.error(), "count": data.count()}
                        self.set_cache(hash_payload, cache_data)
                        sys.stdout.flush()
                    else:
                        self._data = None
                        self._error = data.error()
                    return self
            else:
                data = self._db.select(table, field, condition, sort, top, offset)
                if data is None:
                    self._data = None
                    return self
                if data.error()==False:
                    if is_first is True:
                        if data.count():
                            self._data = data.first()
                        else:
                            self._data = None
                    else:
                        data_len = len(data.result())
                        if data_len>0:
                            self._data = data.result()
                        else:
                            self._data = None
                else:
                    self._data = None
                    self._error = data.error()
                return self
                

        except Exception as e:
            print(e)

    def insert(self, table, condition):
        data = self._db.insert(table, condition)
        if data.count():
            self._data = data.count()
        else:
            self._data = None
            self._error = data.error()
        return self

    def update(self, table, condition):
        data = self._db.update(table, condition)
        if data.count():
            self._data = data.count()
        else:
            self._data = None
            self._error = data.error()
        return self

    def delete(self, table, condition):
        data = self._db.delete(table, condition)
        if data.count():
            self._data = data.count()
        else:
            self._data = None
            self._error = data.error()
        return self

    def exec(self, proc, condition):
        return self._db.exec(proc, condition)

    def get_version(self):
        return self._db.get_version()

    def exists(self):
        if self.data() is not None:
            return True
        else:
            return False

    @staticmethod
    def get_cache(cache_hash):
        data = Model('ReaRedis').select(11, None, {
            0: {'col': 'Local_Model_Cache',
                'operator': '=', 'value': cache_hash}}).data()
        return data

    @staticmethod
    def set_cache(cache_hash, data):
        data = ReaPy.json().dumps(data, default=ReaPy.presenter().datetime_handler)
        #TODO: bazi datalarda json load edemeyip patladigi icin try cachede replace kaldirmak sorunu cozdu
        try:
            epsg_json = ReaPy.json().loads(data.replace("\'", '"'))
        except Exception as e:
            epsg_json = ReaPy.json().loads(data)  
        sys.stdout.flush()
        insert_cache = Model('ReaRedis').insert(11, {
            0: {'Local_Model_Cache:' + cache_hash: {'data': epsg_json, }}}).data()
        sys.stdout.flush()
        return insert_cache
