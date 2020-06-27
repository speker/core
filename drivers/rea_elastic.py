# -*- coding: utf-8 -*-

from core.reapy import ReaPy


class ReaElastic(object):
    __instance = None
    __db = None
    __count = 0
    __error = None
    __result = []
    __configurations = None

    def __init__(self):
        super(ReaElastic).__init__()
        if ReaElastic.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ReaElastic.__instance = self

    @staticmethod
    def get_instance(configurations=None):
        ReaElastic.__configurations = configurations
        # Elastic.connect()
        if ReaElastic.__instance is None:
            ReaElastic.__instance = ReaElastic()
        return ReaElastic.__instance
