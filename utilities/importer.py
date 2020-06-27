# -*- coding: utf-8 -*-

import importlib
import inspect

err_list = []


class Importer:

    def __init__(self):
        self.module_name = None
        self.module = None

        self.object_name = None
        self.object = None

        self.method_name = None

        self.class_list = {}
        self.method_list = []
        self.params = None

    def load_module(self, module_name):
        try:
            m = importlib.import_module(module_name)
            self.module_name = module_name
            self.module = m

            for key in dir(self.module):
                if isinstance(getattr(self.module, key), type) and not key.startswith("__"):
                    self.class_list[key.lower()] = self.load_class(key).get_method_list()

            return self
        except Exception as e:
            print(e)
            return None

    def load_class(self, class_name):
        self.object_name = class_name
        c = getattr(self.module, class_name)

        self.object = c
        self.method_list = []
        for func in dir(c):
            try:
                if func == "__run__":
                    self.method_list.append("")
                else:
                    if not func.startswith("__"):
                        try:
                            self.method_list.append({func: self.get_params(func)})
                        except AttributeError as e:
                            print(str(e))

            except Exception as e:
                err_list.append(str(e))

        return self

    @staticmethod
    def get_source(obj, remove_self=False):
        source = inspect.getsource(obj).lstrip()
        if remove_self is False:
            return source
        else:
            return source.replace('self,', '')

    def get_params(self, func):
        params = inspect.getfullargspec(getattr(self.get_object(), func)).args[1:]
        return params

    def get_object(self):
        return self.object

    def get_class_list(self):
        return self.class_list

    def get_method_list(self):
        return self.method_list

    @staticmethod
    def module_class(module_name, class_name):
        m = importlib.import_module(module_name)
        c = getattr(m, class_name)
        return c

    def set_params(self, params):
        self.params = params
        return self

    def get_module_name(self):
        return self.module_name

    def get_object_name(self):
        return self.object_name

    def get_method(self, name):
        return getattr(self.object(), name)

    def run(self, method=None):
        if method is not None:
            if self.params is None:
                if len(self.get_params(method)) <= 0:
                    try:
                        return getattr(self.object(), method)()
                    except AttributeError as e:
                        print(e)
                else:
                    return -1
            else:
                if len(self.get_params(method)) > 0:
                    try:
                        return getattr(self.object(), method)(*self.params)
                    except Exception as e:
                        print(e)
                else:
                    return -1
        else:
            try:
                return self.object().__run__()
            except Exception as e:
                print(str(e))
