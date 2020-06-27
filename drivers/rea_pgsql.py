# -*- coding: utf-8 -*-

from core.reapy import ReaPy


class ReaPgsql:
    __instance = None
    __db = None
    __count = 0
    __error = None
    __result = []
    __configurations = None
    coll = None
    _count_data = False 
    __get_count = 0

    def __init__(self):
        super(ReaPgsql).__init__()
        if ReaPgsql.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ReaPgsql.__instance = self

    @staticmethod
    def get_instance(configurations=None):
        ReaPgsql.__configurations = configurations
        ReaPgsql.connect()
        if ReaPgsql.__instance is None:
            ReaPgsql.__instance = ReaPgsql()
        return ReaPgsql.__instance

    @staticmethod
    def connect():
        try:
            if ReaPgsql.__configurations is None:
                configurations = ReaPy.configuration().get_configuration()['system']['tcp_server']['pg_sql']
            else:
                configurations = ReaPgsql.__configurations
            try:
                ReaPgsql.__db = ReaPy.pg_sql().connect(user=configurations['user'],
                                                       password=configurations['password'],
                                                       host=configurations['host'],
                                                       port=configurations['port'],
                                                       database=configurations['database'])
                ReaPgsql.__db.autocommit = True
            except Exception as exc:
                print('pge1', exc)
                ReaPgsql.__db.close()
                ReaPgsql.__instance = None
        except (Exception, ReaPy.pg_sql().DatabaseError) as error:
            print('pge2', error)

    def select(self, table, field=None, condition=None, sort=None, top=None, offset=None):
        try:
            sort_param = ''
            top_param = ''
            offset_param = ''
            conditions = ''
            conditions_value = []
            if 'pg_function.' in table:
                action_param = 'SELECT ' + table.replace('pg_function.', '')
            else:
                action_param = 'SELECT * FROM ' + table
            if field is not None:
                action_param = 'SELECT ' + str(field) + ' FROM ' + table
            if field == 'COUNT(*)':
                action_param = 'SELECT COUNT(*) FROM ' + table
            if sort is not None:
                sort_param = 'order by ' + sort
            if top is not None:
                top_param = ' limit ' + str(top)
            if offset is not None:
                offset_param = ' offset ' + str(offset)
            if condition is not None and condition!='':
                condition_params = ReaPy.presenter().sql_condition_presenter(condition, ReaPy.inspect().stack()[0][3])
                conditions = condition_params['condition']
                conditions_value = condition_params['values']
            select_clause = action_param + ' ' + conditions + sort_param + top_param + offset_param
            if self._count_data:
                select_clause_count = "SELECT COUNT(*) as count FROM "+table+ ' ' + conditions
                self.query_count({'query': select_clause_count, 'params': conditions_value}, True)
            self.query({'query': select_clause, 'params': conditions_value}, True)
            return self
        except Exception as e:
            print(e)

    def insert(self, table, condition):
        try:
            value_param = []
            value_params = []
            condition_params = ReaPy.presenter().sql_condition_presenter(condition, ReaPy.inspect().stack()[0][3])
            key_len = int(len(condition_params['insert_key']))
            value_len = int(len(condition_params['insert_value']))
            condition_len = int(value_len / key_len)
            for _ in range(condition_len):
                for _ in range(0, key_len):
                    value_param.append('%s')
                value_params.append('(' + ','.join(value_param) + ')')
                value_param = []
            insert_keys = ','.join(condition_params['insert_key'])
            insert_clause = 'INSERT INTO ' + table + ' (' + insert_keys + ') VALUES ' + ','.join(value_params)
            self.query({'query': insert_clause, 'params': condition_params['insert_value']})
            return self
        except Exception as e:
            print(e)

    def update(self, table, condition):
        try:
            conditions = ''
            condition_values = []
            condition_params = ReaPy.presenter().sql_condition_presenter(condition, ReaPy.inspect().stack()[0][3])
            if 'CONDITION' in condition and condition['CONDITION']:
                conditions = ' ' + condition_params['condition']
                condition_values = condition_params['condition_value']
            values = condition_params['set_value'] + condition_values
            update_clause = 'UPDATE ' + table + ' SET ' + ', '.join(
                condition_params['set_key']) + conditions
            self.query({'query': update_clause, 'params': values})
            return self
        except Exception as e:
            print(e)

    def delete(self, table, condition):
        try:
            if condition is not None:
                condition_params = ReaPy.presenter().sql_condition_presenter(condition, ReaPy.inspect().stack()[0][3])
                conditions = condition_params['condition']
                conditions_value = condition_params['values']
            else:
                conditions = ''
                conditions_value = []
            delete_clause = 'DELETE FROM ' + table + ' ' + conditions
            self.query({'query': delete_clause, 'params': conditions_value})
            return self
        except Exception as e:
            print(e)

    def exec(self, proc, condition):
        self.__count = 0
        self.__error = False
        self.__result = []

        cur = self.__db.cursor()
        cur.execute(proc, condition)
        self.__count = cur.rowcount
        self.__result = cur.fetchall()
        self.__db.close()

    def query(self, sql, fetch=False):
        self.__count = 0
        self.__error = False
        self.__result = []
        self.coll = None

        cur = self.__db.cursor()
        cur.execute(sql['query'], sql['params'])
        self.__count = cur.rowcount
        if fetch is True:
            self.coll = [column[0] for column in cur.description]
            self.__result = cur.fetchall()
        self.__db.close()

    def query_count(self, sql, fetch=False):
        cur = self.__db.cursor()
        cur.execute(sql['query'], sql['params'])
        if fetch is True:
            self.__get_count = cur.fetchone()

    def count(self):
        return self.__count

    def count_data(self):
        self._count_data = True
        return self.__get_count

    def error(self):
        return self.__error

    def result(self):
        return self.__result

    def first(self):
        return [self.__result[0]]

    def get_version(self):
        cur = self.__db.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        return version
