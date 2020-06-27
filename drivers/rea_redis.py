# -*- coding: utf-8 -*-
import operator

from core.reapy import ReaPy


class ReaRedis(object):
    __instance = None
    __db = None
    __count = 0
    __error = None
    __result = []
    __configurations = None
    __pep8 = None
    coll = None

    def __init__(self):
        super(ReaRedis).__init__()
        if ReaRedis.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ReaRedis.__instance = self

    @staticmethod
    def get_instance(configurations=None):
        ReaRedis.__configurations = configurations
        if ReaRedis.__instance is None:
            ReaRedis.__instance = ReaRedis()
        return ReaRedis.__instance

    @staticmethod
    def connect(db):
        try:
            if ReaRedis.__db is None:
                if ReaRedis.__configurations is None:
                    configurations = ReaPy.configuration().get_configuration()['system']['tcp_server']['redis']
                else:
                    configurations = ReaRedis.__configurations
                ReaRedis.__db = ReaPy.redis(host=configurations['host'],
                                            port=configurations['port'],
                                            db=db, password=configurations['redis_auth'])

        except (Exception, ReaPy.kafka_error()) as error:
            print(error)

    def key_exists(self, key):
        result = self.__db.exists(key)
        if result:
            return True
        else:
            return False

    def key_scan(self, key):
        result_keys = []
        result = self.__db.scan(0, key, 10000)
        for key in result[1]:
            result_keys.append(key.decode('utf-8'))

        return result_keys if result_keys else None

    def condition_scan(self, namespace, condition_value, condition_operator, keys_lists):
        ops = {'=': operator.eq,
               '!=': operator.ne,
               '<=': operator.le,
               '>=': operator.ge,
               '>': operator.gt,
               '<': operator.lt}
        key = namespace + '*' if namespace else '*'
        result = self.key_scan(key)
        for keys in result:
            convert_key = keys
            if key != '*':
                convert_key = keys.split(':')
                convert_key = convert_key[len(convert_key) - 1]
            type_convert = ReaPy.transformer().type_converter(condition_value, convert_key)
            if type_convert is not None and ops[condition_operator](type_convert, condition_value) is True:
                keys_lists.append(keys)
        return keys_lists if keys_lists else None

    def find_key(self, condition):
        condition_namespace = condition['key']
        condition_value = condition['value']
        condition_operator = condition['operator']
        keys_list = []
        scan_operators = ['=', '>', '<', '>=', '<=', '!=']
        try:
            namespace = condition_namespace + ':' if condition_namespace else condition_namespace
            if isinstance(condition_value, dict):
                condition_value = ReaPy.json().dumps(condition_value)
            if condition_operator in scan_operators:
                self.condition_scan(namespace, condition_value, condition_operator, keys_list)
            if condition_operator == 'LIKE':
                key = namespace + str(condition_value)
                result = self.key_scan(key)
                if result is not None:
                    keys_list += result
        except ValueError:
            pass
        return keys_list if keys_list else None

    def select(self, db, field=None, condition=None, sort=None, top=None, is_first=False):
        self.__pep8 = {str(field), sort, top, is_first}
        self.__count = 0
        self.__error = False
        self.__result = []
        self.connect(db)
        self.__db.execute_command('SELECT ' + str(db))
        i = 0
        try:
            if condition is not None:
                condition_params = ReaPy.presenter().redis_where_condition(condition)
                for c_key in condition_params:
                    db_key = self.find_key(c_key)
                    if db_key is not None:
                        for key in db_key:
                            result = self.__db.get(key)
                            ttl = self.__db.ttl(key)
                            self.__result.append((key, result.decode('utf-8')))
                            self.__result.append(ttl)
                            i += 1
            else:
                for key in self.__db.scan_iter():
                    result = self.__db.get(key)
                    ttl = self.__db.ttl(key)
                    self.__result.append((key.decode('utf-8'), result.decode('utf-8')))
                    self.__result.append(ttl)
                    i += 1
        except (Exception, ReaPy.redis_error()) as error:
            print(error)
            self.__error = error
        self.__count = i
        return self

    def update(self, db, condition):
        selected_db = db
        self.__count = 0
        self.__error = False
        self.__result = []
        if isinstance(db, list):
            selected_db = db[0]
            ttl = db[1]
        else:
            ttl = None
        self.connect(selected_db)
        self.__db.execute_command('SELECT ' + str(selected_db))

        update_value = condition['SET']

        if isinstance(update_value, dict):
            update_value = ReaPy.json().dumps(update_value)
        else:
            update_value = ', '.join(update_value)
        i = 0
        try:
            if condition['CONDITION'] is not None:
                condition_params = ReaPy.presenter().redis_where_condition(condition['CONDITION'])
                for c_key in condition_params:
                    db_key = self.find_key(c_key)
                    if db_key is not None:
                        for key in db_key:
                            self.__db.set(key, str(update_value), ttl)
                            i += 1
        except (Exception, ReaPy.redis_error()) as error:
            self.__error = error
        self.__count = i
        return self

    def delete(self, db, condition):
        self.__count = 0
        self.__error = False
        self.__result = []
        self.connect(db)
        self.__db.execute_command('SELECT ' + str(db))
        i = 0
        try:
            if condition is not None:
                condition_params = ReaPy.presenter().redis_where_condition(condition)
                for c_key in condition_params:
                    db_key = self.find_key(c_key)
                    if db_key is not None:
                        for key in db_key:
                            self.__db.delete(key)
                            i += 1
            else:
                for key in self.__db.scan_iter():
                    self.__db.delete(key)
                    i += 1
        except (Exception, ReaPy.redis_error()) as error:
            self.__error = error
        self.__count = i
        return self

    def insert(self, db, condition):
        ttl = None
        selected_db = db
        self.__count = 0
        self.__error = False
        self.__result = []
        if isinstance(db, list):
            selected_db = db[0]
            ttl = db[1]
        self.connect(selected_db)
        self.__db.execute_command('SELECT ' + str(selected_db))
        i = 0
        ins_condition_params = ReaPy.presenter().redis_insert_condition(condition)
        for c_key, c_value in ins_condition_params.items():
            for i_key, i_value in c_value.items():
                try:
                    if isinstance(i_value, dict):
                        i_value = ReaPy.json().dumps(i_value)
                    self.__db.set(str(i_key), i_value, ttl)
                    i += 1
                except (Exception, ReaPy.redis_error()) as error:
                    self.__error = error
                self.__count = i
        return self

    def count(self):
        return self.__count

    def error(self):
        return self.__error

    def result(self):
        return self.__result
