# -*- coding: utf-8 -*-
from datetime import datetime
from functools import reduce
import operator


class Find:

    @staticmethod
    def in_dict(key, value, dictionary):
        result = {k: v for k, v in dictionary.items() if v[key] == value}
        if result:
            return result
        else:
            return None

    @staticmethod
    def in_dict_by_value(value, dictionary):
        for d_key, d_value in dictionary.items():
            if d_value == value:
                return d_key

    @staticmethod
    def get_from_nested_template_dict(dict_data, map_list):
        new_dict = []
        try:
            if isinstance(map_list, dict):
                for key, value in map_list.items():
                    if value[0] == 'rea_binding':
                        new_dict.append(value[1])
                    else:
                        if 'capitalize' not in value:
                            new_dict.append(str(reduce(operator.getitem, value, dict_data)))
                        else:
                            del value[-1]
                            new_dict.append(str(reduce(operator.getitem, value, dict_data)).title())

                return "".join(new_dict)
            else:
                if map_list[0] == 'rea':
                    if map_list[1] == 'date_dmy':
                        return datetime.today().strftime('%d.%m.%Y')
                else:
                    return reduce(operator.getitem, map_list, dict_data)
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_from_nested_dict(dict_data, map_list):
        try:
            return reduce(operator.getitem, map_list, dict_data)
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_all_keys_from_nested_dict(data, store=None, last_key=''):
        if store is None:
            store = {}
        for keys in data:
            child = data[keys]
            if isinstance(child, dict):
                last_key += keys + ','
                Find.get_all_keys_from_nested_dict(child, store, last_key)
            else:
                stored_value = last_key + keys
                store[keys] = stored_value.split(',')
        return store

    @staticmethod
    def in_nested_dict_by_value(dict_data, find_value):
        all_value = {}
        all_keys = Find.get_all_keys_from_nested_dict(dict_data)
        for v_key in find_value:
            for d_key, d_value in all_keys.items():
                dict_value = Find.get_from_nested_dict(dict_data, d_value)
                if v_key == dict_value:
                    all_value[v_key] = d_key
        return all_value
