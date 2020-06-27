# -*- coding: utf-8 -*-
import json
import fastjsonschema
from core.helpers.transformer import Transformer


class Validator:

    @staticmethod
    def number_control(listed):
        i = 0
        while i < len(listed):
            if isinstance(listed[i], (float, int)):
                i += 1
                if i >= len(listed):
                    return True, listed
            else:
                i += 1
                return Validator.call_number_control(listed, i)

    @staticmethod
    def call_number_control(listed, i):
        try:
            listed[i - 1] = Transformer.ohb_to_all(listed[i - 1], float)[0]
            if i >= len(listed):
                return True, listed
        except ValueError or TypeError:
            print(ValueError, TypeError)
            if i >= len(listed):
                return False, listed

    @staticmethod
    def json_validate_file(path, data):
        try:
            if path and data:
                with open(path, "r") as file:
                    schema_file = json.load(file)
                validator = fastjsonschema.compile(schema_file)
                print("Schema : ", schema_file, "\n", "Data : ", data)
                return validator(data)
            else:
                print("Path or Data is INVALID!!")
        except Exception as e:
            print(e)

    @staticmethod
    def json_validate(schema, data):
        try:
            if schema and data:
                validator = fastjsonschema.compile(schema)
                validator(data)
                return {'success': True}
            else:
                return {'success': False, 'message': 'missing data'}
        except fastjsonschema.JsonSchemaException as exp:
            message = str(exp)
            return {'success': False, 'message': message}

    @staticmethod
    def is_json(json_data):
        try:
            json.loads(json_data)
        except ValueError:
            return False
        return True

    @staticmethod
    def is_valid_tc_id_number(id_number):
        id_number = str(id_number)
        if not len(id_number) == 11:
            return False
        if not id_number.isdigit():
            return False
        if int(id_number[0]) == 0:
            return False
        digits = [int(d) for d in str(id_number)]
        if not sum(digits[:10]) % 10 == digits[10]:
            return False
        if not (((7 * sum(digits[:9][-1::-2])) - sum(digits[:9][-2::-2])) % 10) == digits[9]:
            return False
        return True
