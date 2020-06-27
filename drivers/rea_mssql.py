# -*- coding: utf-8 -*-
import json

from core.reapy import ReaPy


class ReaMssql(object):
    __instance = None
    __db = None
    __count = 0
    __error = None
    __result = []
    __configurations = None
    coll = None

    def __init__(self):
        super(ReaMssql).__init__()
        if ReaMssql.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ReaMssql.__instance = self

    @staticmethod
    def get_instance(configurations=None):
        ReaMssql.__configurations = configurations
        ReaMssql.connect()
        if ReaMssql.__instance is None:
            ReaMssql.__instance = ReaMssql()
        return ReaMssql.__instance

    @staticmethod
    def connect():
        try:
            if ReaMssql.__configurations is None:
                configurations = ReaPy.configuration().get_configuration()['system']['tcp_server']['ms_sql']
            else:
                configurations = ReaMssql.__configurations
            try:
                connection_string = 'Driver={ODBC Driver 17 for SQL Server};Server=' + configurations['host'] + ',' + str(configurations[
                                                                                                           'port']) + ';Database=' + \
                                    configurations['database'] + ';UID=' + configurations['user'] + ';PWD=' + \
                                    configurations['password'] + ';'
                ReaMssql.__db = ReaPy.ms_sql().connect(connection_string)
            except Exception as exc:
                print(exc)

        except (Exception, ReaPy.ms_sql().DatabaseError) as error:
            print(error)

    def select(self, table, field=None, condition=None, sort=None, top=None):
        sort_param = ''
        top_param = ''
        conditions = ''
        if top is not None:
            top_param = ' TOP ' + str(top)
        action_param = 'SELECT ' + top_param + ' * FROM ' + table
        if field is not None:
            action_param = 'SELECT ' + top_param + str(field) + ' FROM ' + table
        if sort is not None:
            sort_param = 'order by ' + sort
        if condition is None:
            conditions_value = None
        else:
            condition_params = ReaPy.presenter().sql_condition_presenter(condition, ReaPy.inspect().stack()[0][3])
            conditions = condition_params['condition']
            conditions_value = condition_params['values']
        select_clause = action_param + ' ' + conditions + sort_param

        self.query({'query': select_clause, 'params': conditions_value}, True)
        return self

    def insert(self, table, condition):
        condition_params = ReaPy.presenter().sql_condition_presenter(condition, ReaPy.inspect().stack()[0][3])
        value_param = []
        value_params = []
        value_len = int(len(condition_params['insert_value']))
        key_len = int(len(condition_params['insert_key']))
        condition_len = int(value_len / key_len)
        for _ in range(0, condition_len):
            for _ in range(key_len):
                value_param.append('%s')
            value_params.append('(' + ','.join(value_param) + ')')
            value_param = []
        insert_keys = ','.join(condition_params['insert_key'])
        insert_clause = 'INSERT INTO ' + table + ' (' + insert_keys + ') VALUES ' + ','.join(value_params)
        self.query({'query': insert_clause, 'params': condition_params['insert_value']})
        return self

    def update(self, table, condition):
        condition_params = ReaPy.presenter().sql_condition_presenter(condition, ReaPy.inspect().stack()[0][3])
        if 'CONDITION' not in condition and not condition['CONDITION']:
            conditions = ''
            condition_values = []
        else:
            conditions = ' ' + condition_params['condition']
            condition_values = condition_params['condition_value']
        values = condition_params['set_value'] + condition_values
        update_clause = 'UPDATE ' + table + ' SET ' + ', '.join(
            condition_params['set_key']) + conditions
        self.query({'query': update_clause, 'params': values})
        return self

    def delete(self, table, condition):
        if condition is None:
            conditions = ''
            conditions_value = []
        else:
            condition_params = ReaPy.presenter().sql_condition_presenter(condition, ReaPy.inspect().stack()[0][3])
            conditions = condition_params['condition']
            conditions_value = condition_params['values']
        delete_clause = 'DELETE FROM ' + table + ' ' + conditions
        self.query({'query': delete_clause, 'params': conditions_value})
        return self

    def exec(self, proc, condition):
        self.__count = 0
        self.__error = False
        self.__result = []
        try:
            cur = self.__db.cursor()
            cur.callproc(proc, condition)
            self.__count = cur.rowcount
            self.__result = cur.fetchall()
            self.__db.commit()
        except (Exception, ReaPy.ms_sql().DatabaseError) as error:
            print(error)

    def query(self, sql, fetch=False):
        self.__count = 0
        self.__error = False
        self.__result = []
        self.coll = None
        try:
            cur = self.__db.cursor()
            if sql['params'] is not None:
                query = sql['query'].replace("%s", "?")
                cur.execute(query, sql['params'])
            else:
                cur.execute(sql['query'])
            self.__count = cur.rowcount
            if fetch is True:
                self.coll = [column[0] for column in cur.description]
                self.__result = cur.fetchall()
            self.__db.commit()
        except (Exception, ReaPy.ms_sql().DatabaseError) as error:
            self.__error = error

    def count(self):
        return self.__count

    def error(self):
        return self.__error

    def result(self):
        return self.__result

    def first(self):
        return [self.__result[0]]

    def get_version(self):
        cur = self.__db.cursor()
        cur.execute("SELECT @@VERSION")
        version = cur.fetchone()
        return version
