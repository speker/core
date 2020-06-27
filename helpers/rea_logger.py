# -*- coding: utf-8 -*-
import json

from core.utilities.kafka_logger import KafkaLogger


class ReaLogger:
    conn = None

    def __init__(self):
        super(ReaLogger).__init__()
        self.conn = KafkaLogger.get_instance()

    def write_log(self, topic, data):
        if self.conn._KafkaLogger__db is not None:
            self.conn.write_log(topic, data)

