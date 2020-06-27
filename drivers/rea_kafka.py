# -*- coding: utf-8 -*-

from core.reapy import ReaPy


class ReaKafka(object):
    __instance = None
    __db = None
    __count = 0
    __error = None
    __result = []
    __configurations = None
    __pep8 = None
    coll = None
    func_error = 'kafka only supports insert operation'

    def __init__(self):
        super(ReaKafka).__init__()
        if ReaKafka.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ReaKafka.__instance = self

    @staticmethod
    def get_instance(configurations=None):
        ReaKafka.__configurations = configurations
        ReaKafka.connect()
        if ReaKafka.__instance is None:
            ReaKafka.__instance = ReaKafka()
        return ReaKafka.__instance

    @staticmethod
    def connect():
        try:
            if ReaKafka.__db is None:
                if ReaKafka.__configurations is None:
                    configurations = ReaPy.configuration().get_configuration()['system']['tcp_server']['kafka']
                else:
                    configurations = ReaKafka.__configurations
                ReaKafka.__db = ReaPy.kafka_producer(value_serializer=lambda m: ReaPy.json().dumps(m).encode('ascii'),
                                                     bootstrap_servers=configurations['host'] + ':' + str(
                                                         configurations[
                                                             'port']), retries=3)

        except (Exception, ReaPy.kafka_error()) as error:
            print(error)

    def select(self, topic, field=None, condition=None, sort=None, top=None, is_first=False):
        self.__pep8 = {topic, str(field), str(condition), sort, top, is_first}
        self.__count = 0
        self.__error = self.func_error
        self.__result = []
        return self

    def update(self, topic, condition):
        self.__pep8 = {topic, str(condition)}
        self.__count = 0
        self.__error = self.func_error
        self.__result = []
        return self

    def delete(self, topic, condition):
        self.__pep8 = {topic, str(condition)}
        self.__error = self.func_error
        self.__count = 0
        self.__result = []
        return self

    def insert(self, topic, condition):
        condition_params = ReaPy.presenter().kafka_insert_condition(condition)
        self.query(topic, condition_params)
        return self

    def query(self, topic, condition):
        self.__count = 0
        self.__error = False
        self.__result = []
        try:
            i = 0
            for c_key, c_value in condition.items():
                self.__db.send(topic, c_value)
                i += 1
            self.__count = i
            self.__db.flush()
        except (Exception, ReaPy.kafka_error()) as error:
            self.__error = error

    def count(self):
        return self.__count

    def error(self):
        return self.__error

    def result(self):
        return self.__result
