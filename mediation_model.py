# -*- coding: utf-8 -*-

from core.reapy import ReaPy
from core.drivers.rea_mediation import ReaMediation
import math

class MediationModel(object):
    _db = None
    _data = []
    _error = None
    pagination_offset = 0
    count_data = False
    _aktif_mi = None

    def __init__(self, source_id=None):
        configurations = ReaPy.configuration().get_configuration()['system']['mediation_server']
        self._db = ReaMediation.get_instance(configurations, source_id)

    def data(self):
        try:
            if self._db.coll is not None:
                results = []
                if self._data is not None:
                    for row in self._data:
                        results.append(dict(zip(self._db.coll, row)))
                    if self.count_data:
                        count_data = self._db.count_data()
                        try:
                            count_data = count_data[0]
                        except:
                            count_data = 0
                        total_page = math.ceil(int(count_data)/int(self.pagination_offset))
                        return results,count_data,total_page
                    else:
                        return results
            else:
                if self.count_data:
                    count_data = self._db.count_data()
                    try:
                        count_data = count_data[0]
                    except:
                        count_data = 0
                    total_page = math.ceil(int(count_data)/int(self.pagination_offset))
                    return self._data,count_data,total_page
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

    def select(self, table, field=None, condition=None, sort=None, top=None, is_first=False, cache=False,offset=None):
        data = self._db.select(table, field, condition, sort, top, cache, offset)
        if data.count():
            if is_first is True:
                self._data = data.first()
            else:
                self._data = data.result()
        else:
            self._data = None
            self._error = data.error()

        return self

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


