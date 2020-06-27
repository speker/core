# -*- coding: utf-8 -*-
import inspect
import json
import sys
from pathlib import Path
from types import FunctionType
import platform
from core.helpers.find import Find
from core.helpers.transformer import Transformer
from datetime import datetime


class Presenter:

    @staticmethod
    def cls_methods(cls):
        methods = [x for x, y in cls.__dict__.items() if type(y) == FunctionType]
        ignore = methods.index(sys._getframe(1).f_code.co_name)
        del methods[ignore]
        return methods

    @staticmethod
    def rea_log_formatter(response_header, request, response, status):
        environ = request.environ
        new_env = {}
        if environ is not None:
            for key, value in environ.items():
                if isinstance(value, str) or isinstance(value, tuple) or isinstance(value, bool) or isinstance(value,
                                                                                                               bool):
                    new_env[key] = value
        if 'result' in response:
            i = 0
            for results in response['result']:
                for r_key, r_value in results.items():
                    if type(r_value) is datetime:
                        response['result'][i][r_key] = str(r_value)
                i += 1
        log_data = {
            'response_id': response_header['response_id'],
            'container_id': response_header['container_id'],
            'now': response_header['now'],
            'http_status': status,
            'request': {
                'base_url': request.base_url,
                'headers': new_env,
                'charset': request.charset,
                'authorization': request.authorization,
                'method': request.method,
                'files': {k: v for k, v in request.files.items()},
                'form': {k: v for k, v in request.form.items()},
                'json': request.json,
            },
            'response': response
        }
        return log_data

    @staticmethod
    def string_to_date(date_string):
        result = None
        date_formats = ["%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y", "%Y/%m/%d", "%d/%m/%Y", "%m/%d/%Y", "%Y.%m.%d", "%d.%m.%Y",
                        "%m.%d.%Y", "%c", "%x", "%Y-%m-%d %H:%M:%S"]
        for f_value in date_formats:
            try:
                datetime.strptime(date_string, f_value)
                result = f_value
            except ValueError as e:
                print(e)
                continue
        return result

    @staticmethod
    def get_message(path, tag):
        try:
            if path and tag:
                with open(path, "r", encoding='utf8') as file:
                    data = json.load(file)
                    return data[tag]
            else:
                print("Path is INVALID")
        except Exception as e:
            print(e)

    @staticmethod
    def get_schema(path, tag):
        try:
            if path and tag:
                with open(path, "r", encoding='utf8') as file:
                    data = json.load(file)
                    return data[tag]
            else:
                print("Path is INVALID", flush=True)
        except Exception as e:
            print(e, flush=True)

    @staticmethod
    def data_to_source_replacer(source, data):
        try:
            find_keys = Find.in_nested_dict_by_value(source, data)
            source_keys = Find.get_all_keys_from_nested_dict(source)
            for f_key, f_value in find_keys.items():
                Transformer().set_in_nested_dict(source, source_keys[f_value], data[f_key])
            return source
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def sql_condition_presenter(condition, action):
        presenter_error = []
        actions = ['select', 'insert', 'delete', 'update']
        if action not in actions:
            presenter_error.append('expression action error')

        if not condition or not isinstance(condition, dict):
            presenter_error.append('condition dict error')

        if not presenter_error:
            call_action = getattr(Presenter, 'sql_' + action + '_condition')
            return call_action(condition)
        else:
            return presenter_error

    @staticmethod
    def set_sql_scope(scope):
        if not scope:
            scope_start = '( '
            scope_stop = ''
        else:
            scope_start = ''
            scope_stop = ') '
        return {'scope_start': scope_start, 'scope_stop': scope_stop}

    @staticmethod
    def sql_where_condition(condition):
        condition_error = []
        conditions = []
        condition_values = []
        for c_key, c_param in condition.items():
            combiner = ''
            operators = ['=', '>', '<', '>=', '<=', '!=', 'LIKE', 'IS', 'IS NOT']
            combiners = ['AND', 'OR']
            scopes = [0, 1]
            get_scope = {'scope_start': '', 'scope_stop': ''}

            if not all(k in c_param for k in ('col', 'operator', 'value')):
                condition_error.append('condition [' + str(c_key) + '] : ' + str(c_param) + ' have error')

            if 'operator' in c_param and c_param['operator'] not in operators:
                condition_error.append('condition [' + str(c_key) + '] :  have operator error')

            if 'combiner' in c_param and c_param['combiner'] in combiners:
                combiner = c_param['combiner']

            if 'scope' in c_param and c_param['scope'] in scopes:
                get_scope = Presenter.set_sql_scope(c_param['scope'])

            condition_values.append(c_param['value'])
            condition_param = str(get_scope['scope_start']) + str(c_param['col']) + ' ' + str(
                c_param['operator']) + ' %s ' + str(get_scope['scope_stop']) + str(combiner)
            conditions.append(condition_param)

        if condition_error:
            return condition_error
        else:
            return {'condition': 'WHERE ' + ' '.join(conditions), 'values': condition_values}

    @staticmethod
    def redis_where_condition(condition):
        condition_error = []
        conditions = []
        for c_key, c_param in condition.items():
            operators = ['=', '>', '<', '>=', '<=', '!=', 'LIKE']
            if not all(k in c_param for k in ('value', 'operator', 'col')):
                condition_error.append('condition [' + str(c_key) + '] : ' + str(c_param) + ' have error')
            if 'operator' in c_param and c_param['operator'] not in operators:
                condition_error.append('condition [' + str(c_key) + '] :  have operator error')
            conditions.append({'key': c_param['col'], 'operator': c_param['operator'], 'value': c_param['value']})
        if condition_error:
            return condition_error
        else:
            return conditions

    @staticmethod
    def sql_select_condition(condition):
        condition_params = Presenter.sql_where_condition(condition)
        return condition_params

    @staticmethod
    def sql_insert_condition(condition):
        insert_keys = []
        insert_values = []
        for c_key, c_value in condition.items():
            for d_key, d_value in c_value.items():
                if d_key not in insert_keys:
                    insert_keys.append(d_key)
                if isinstance(d_value, dict):
                    d_value = json.dumps(d_value)
                insert_values.append(d_value)
        insert_clause = {'insert_key': insert_keys, 'insert_value': insert_values}
        return insert_clause

    @staticmethod
    def kafka_insert_condition(condition):
        condition_error = []
        if not condition or not isinstance(condition, dict):
            condition_error.append('condition dict error')
        if condition_error:
            return condition_error
        return condition

    @staticmethod
    def redis_insert_condition(condition):
        condition_error = []
        if not condition or not isinstance(condition, dict):
            condition_error.append('condition dict error')
        if condition_error:
            return condition_error
        return condition

    @staticmethod
    def sql_update_condition(condition):
        set_keys = []
        set_values = []
        for c_key, c_value in condition['SET'].items():
            set_keys.append(c_key + ' = %s')
            if isinstance(c_value, dict):
                c_value = json.dumps(c_value)
            set_values.append(c_value)
        update_clause = {'set_key': set_keys, 'set_value': set_values}

        if 'CONDITION' in condition and condition['CONDITION']:
            condition_params = Presenter.sql_where_condition(condition['CONDITION'])
            update_clause['condition'] = condition_params['condition']
            update_clause['condition_value'] = condition_params['values']
        return update_clause

    @staticmethod
    def sql_delete_condition(condition):
        condition_params = Presenter.sql_where_condition(condition)
        return condition_params

    @staticmethod
    def replace_multiple(original, replacer, replaced):
        for elem in replacer:
            if elem in original:
                original = original.replace(elem, replaced)
        return original

    @staticmethod
    def get_socket_remote_port(socket):
        replaced_data = Presenter.replace_multiple(socket, ['<', '>', '(', ')', ' '], '')
        socket_data = replaced_data.split(',')
        return socket_data[7]

    @staticmethod
    def get_project_root() -> Path:
        return Path(__file__).parent.parent.parent

    @staticmethod
    def get_platform():
        return platform.node()

    @staticmethod
    def get_folder_by_date():
        today = datetime.now()
        return today.strftime('/%Y/%m/%d/')

    def format_coupler(self, value, options, img_path):
        couple_string = options['coupler_prefix'] + str(value) + options['coupler_postfix']
        if options['coupler_type'] == 'img':
            couple_string = img_path + couple_string
        if options['coupler_type'] == 'date':
            date_format = self.string_to_date(couple_string)
            couple_string = datetime.strptime(couple_string, date_format).strftime(options['coupler_format'])

        return couple_string

    @staticmethod
    def tr_to_en(tr_str):
        in_tab = "İı"
        out_tab = "Ii"
        tran_tab = str.maketrans(in_tab, out_tab)
        return tr_str.translate(tran_tab)

    @staticmethod
    def get_endpoint_module_name(frame):
        module = inspect.getmodule(frame[0]).__name__
        module_list = module.replace("'", "").split('.')
        return module_list[5] + '/' + module_list[7]

    @staticmethod
    def datetime_handler(x):
        if isinstance(x, datetime):
            return x.isoformat()
        raise TypeError("Unknown type")

    @staticmethod
    def dict_to_trimmer_dict(data):
        trimmed_dict = {}
        for key, value in data.items():
            trimmed_dict[key] = value.strip() if isinstance(value, str) else value
        return trimmed_dict
