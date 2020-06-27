# -*- coding: utf-8 -*-
import json
from core.helpers.find import Find


class Transformer:

    @staticmethod
    def string_to_all(value, convert_type):  # string to float, int
        if convert_type == int or float:
            if isinstance(value, str) and value.isnumeric():
                try:
                    value = float(value)
                    if convert_type == int:
                        value = int(value)
                    return value, type(value)
                except ValueError:
                    print("Hatalı türde veri girişi")
                    return False
            else:
                print("String türünde bir rakamsal değer giriniz.\nSadece int veya float a dönüştürür")
                return False

    @staticmethod
    def flint_to_str(value):  # float, int value convert to string
        try:
            if isinstance(value, (int, float)):
                value = str(value)
            else:
                print("Float veya Int tipinde veri giriniz")
            return value, type(value)
        except ValueError:
            print("Hatalı tür veri")
            return False

    @staticmethod
    def int_to_ohb(value, convert_type):  # int value convert to octal, hexadecimal, binary
        try:
            if isinstance(value, int):
                if convert_type == oct or hex or bin:
                    value = convert_type(value)
                    return value, type(value)
            else:
                print("Int tipinde değişken giriniz")
                return 0
        except ValueError:
            print(Exception)

    @staticmethod
    def containers_convert(container, convert_type):  # list, tuple, set, dict convert each other
        try:
            if isinstance(container, (list, tuple, set, dict)):
                if convert_type == list or dict or set or tuple:
                    container = convert_type(container)
                    return container, type(container)
                else:
                    print("Convert Type yanlış girildi")
                    return False
            else:
                print("Container tipi yanlış girildi")
                return False
        except ValueError or TypeError:
            print(ValueError, TypeError)

    @staticmethod
    def ohb_to_all(value, convert_type):  # octal, hexadecimal, binary to int, float, string
        try:
            value = convert_type(value)
            return value, type(value)
        except TypeError or ValueError:
            print(TypeError)
            print(ValueError)

    @staticmethod
    def type_converter(source_data, change_data):
        value = None
        try:
            if isinstance(source_data, int):
                value = int(change_data)
            if isinstance(source_data, str):
                value = str(change_data)
            if isinstance(source_data, float):
                value = float(change_data)
            if isinstance(source_data, bool):
                value = str(change_data)
            if isinstance(source_data, dict):
                value = json.dumps(change_data)
            return value
        except ValueError as e:
            return None

    @staticmethod
    def set_in_nested_dict(dict_data, map_list, values):
        Find.get_from_nested_dict(dict_data, map_list[:-1])[map_list[-1]] = values
