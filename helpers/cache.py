# -*- coding: utf-8 -*-
from core.utilities import redis


class Cache:

    connection = None

    def __init__(self, system_config):

        if self.connection is None:
            try:
                self.connection = redis.StrictRedis(
                    host=system_config['redis']['host'],
                    port=system_config['redis']['port'],
                    password=system_config['redis']['password'],
                    db=system_config['redis']['default_db'])

                self.connection.ping()

            except Exception as exc:
                print(exc)

    def expire_set(self, key_name, ex):
        try:
            self.connection.expire(key_name, ex)
        except Exception as exc:
            print('Expire SET Error:', str(exc))

    def set_value(self, name, value, ex=None):

        try:
            self.connection.set(name, value, ex)
        except Exception as exc:
            print('Redis SET Error:', str(exc))

    def del_value(self, name):

        try:
            self.connection.delete(name)
        except Exception as exc:
            print('Redis Delete Error:', str(exc))

    def get_value(self, name, value=None):

        try:
            return_val = self.connection.get(name)
        except Exception as exc:
            print('Redis GET Error:', str(exc))
            return_val = value

        return return_val

    def get_all_keys(self, name="*"):
        obj = []
        for key in self.connection.scan_iter(name):
            obj.append(key)

        return obj
