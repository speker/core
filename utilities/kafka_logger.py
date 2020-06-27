import json
import datetime
from threading import Thread
from kafka import KafkaProducer


class KafkaLogger:
    configurations = {'host': 'kafka-headless.kafka', 'port': 9092}
    __db = None
    __instance = None

    def __init__(self):
        super(KafkaLogger).__init__()
        if KafkaLogger.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            KafkaLogger.__instance = self

    def default(o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()

    @staticmethod
    def get_instance():
        KafkaLogger.connect()
        if KafkaLogger.__instance is None:
            KafkaLogger.__instance = KafkaLogger()
        return KafkaLogger.__instance

    @staticmethod
    def connect():
        if KafkaLogger.__db is None:
            try:
                KafkaLogger.__db = KafkaProducer(
                    value_serializer=lambda m: json.dumps(m, default=KafkaLogger.default).encode('ascii'),
                    bootstrap_servers=KafkaLogger.configurations['host'] + ':' + str(
                        KafkaLogger.configurations[
                            'port']), retries=3)

            except Exception as error:
                print(error)

    def write_log(self, topic, data):
        write_kafka = Thread(target=self.write_kafka, args=(topic, data,))
        write_kafka.start()
        write_kafka.join()

    def write_kafka(self, topic, data):
        try:
            self.__db.send(topic, data)
            self.__db.flush()
        except Exception as error:
            print(error)
