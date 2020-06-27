# -*- coding: utf-8 -*-
import datetime
import importlib
import inspect
import json
import os
import platform
import sys
import string
import random
import time
from multiprocessing import Process
from threading import Thread
from datetime import timedelta
import requests
import exception
import ldap
from kafka import KafkaProducer
from kafka.errors import KafkaError
from requests_ntlm import HttpNtlmAuth
from werkzeug.utils import secure_filename
import pyodbc
import core.utilities.rest as rest
import core.utilities.soap as soap
import core.utilities.postgresql as py_pgsql
import core.utilities.redis as redis
import core.utilities.mysql as py_mysql
from .helpers.crypt import Crypt
from .helpers.find import Find
from .helpers.hash import Hash
from .helpers.mail import Mail
from .helpers.presenter import Presenter
from .helpers.rea_math import ReaMath
from .helpers.save import Save
from .helpers.rea_logger import ReaLogger
from .helpers.transformer import Transformer
from .helpers.validator import Validator
from .utilities.configurator import Configuration
from .utilities.importer import Importer
from .utilities.json_server import JsonServer
from .utilities.termcolor import colored
from .utilities.pdf import Template
from .utilities.rest import jsonify, request, Rest, session, Response, render_template, send_from_directory, redirect
from .utilities.session import Session
from .utilities.rest.sessions import SecureCookieSessionInterface
from .utilities.restful import Api
from .utilities.restful import Resource
import locale


class ReaPy:
    request = None
    session_store = None
    kafka_logger_retry = 0

    # locale.setlocale(locale.LC_ALL, 'tr_TR.utf8')

    @staticmethod
    def validator():
        return Validator()

    @staticmethod
    def colored(text, color):
        return colored(text, color)

    @staticmethod
    def sleep(second):
        return time.sleep(second)

    def tcp_server(self):
        JsonServer.master = self
        return JsonServer

    @staticmethod
    def rea_math():
        return ReaMath()

    @staticmethod
    def process(**configs):
        return Process(**configs)

    @staticmethod
    def transformer():
        return Transformer()

    @staticmethod
    def rea_exception():
        return Exception

    @staticmethod
    def importer():
        return Importer()

    @staticmethod
    def configuration():
        return Configuration()

    @staticmethod
    def presenter():
        return Presenter()

    @staticmethod
    def timedelta(**configs):
        return timedelta(**configs)

    @staticmethod
    def inspect():
        return inspect

    @staticmethod
    def platform():
        return platform

    @staticmethod
    def rea_os():
        return os

    @staticmethod
    def rest_api(app):
        return Api(app)

    @staticmethod
    def rest_server(__name__, **configs):
        return Rest(__name__, **configs)

    @staticmethod
    def session(app):
        return Session(app)

    @staticmethod
    def sessions():
        return SecureCookieSessionInterface()

    @staticmethod
    def render_template(template, **context):
        return render_template(template, **context)

    @staticmethod
    def rest_session():
        return session

    @staticmethod
    def rest_server_addition():
        return rest

    @staticmethod
    def rest_request():
        return request

    @staticmethod
    def set_request(data):
        ReaPy.request = data
        return data

    @staticmethod
    def set_session(data):
        session_dict = {}
        for key in data:
            session_dict[key] = data.get(key)
        ReaPy.session_store = data

    @staticmethod
    def redirect(location, code, response=None):
        return redirect(location, code, response)

    @staticmethod
    def rest_resource():
        return Resource

    @staticmethod
    def jsonify(**configs):
        return ReaPy.rest_response(configs['data'])

    @staticmethod
    def get_reactor_source(db_name):
        db_id_list = {
            'yeten': '00cc9318-3773-47c3-818d-e5a864ab0eb5',
            'yeten_dev': '663a08a2-44c3-4306-be08-706552184157'
        }
        return db_id_list[db_name]

    @staticmethod
    def get_response_header():
        response_id = str(ReaPy.hash().get_uuid())
        container_id = ReaPy.presenter().get_platform()
        now = str(ReaPy.now())
        return {'response_id': response_id, 'container_id': container_id, 'now': now}

    @staticmethod
    def rest_response(message, status_code=200):
        try:
            response_header = ReaPy().get_response_header()
            message['response_id'] = response_header['response_id']
            response = jsonify(data=message)
            response.headers['ReActor-Container-Id'] = response_header['container_id']
            response.headers['ReActor-Response-Id'] = response_header['response_id']
            response.headers['ReActor-Response-Time'] = response_header['now']
            response.headers['Content-Security-Policy'] = "default-src 'self'"

            response.status_code = status_code
            try:
                request_data = ReaPy.request
                log_state = ReaPy.configuration().get_configuration()['system']['rest_server']
                if 'no_log' not in log_state:
                    log_data = ReaPy().presenter().rea_log_formatter(response_header, request_data, message,
                                                                     status_code)
                    ReaLogger().write_log('reactor', log_data)
            except Exception as exp:
                print(exp)
            return response
        except Exception as exp:
            print(exp)

    @staticmethod
    def response(**configs):
        html_response = {}
        sessions = ReaPy.session_store
        response_header = ReaPy().get_response_header()
        configs['headers'] = {
            'ReActor-Container-Id': response_header['container_id'],
            'ReActor-Response-Id': response_header['response_id'],
            'ReActor-Response-Time': response_header['now']
        }
        html_response['html_response'] = configs['response']
        try:
            request_data = ReaPy.request
            log_state = ReaPy.configuration().get_configuration()['system']['rest_server']
            if 'no_log' not in log_state:
                log_data = ReaPy().presenter().rea_log_formatter(response_header, request_data, html_response,
                                                                 configs['status'])
                ReaLogger().write_log('reactor', log_data)
        except Exception as exp:
            print(exp)
        return Response(**configs)

    @staticmethod
    def send_from_directory(**configs):
        return send_from_directory(**configs)

    @staticmethod
    def pg_sql():
        return py_pgsql

    @staticmethod
    def ms_sql():
        return pyodbc

    @staticmethod
    def my_sql():
        return py_mysql

    @staticmethod
    def kafka_producer(**configs):
        return KafkaProducer(**configs)

    @staticmethod
    def kafka_error():
        return KafkaError

    @staticmethod
    def redis(**configs):
        return redis.Redis(**configs)

    @staticmethod
    def redis_error():
        return redis.RedisError

    @staticmethod
    def sys():
        return sys

    @staticmethod
    def json():
        return json

    @staticmethod
    def string():
        return string

    @staticmethod
    def random():
        return random

    @staticmethod
    def exception():
        return exception

    @staticmethod
    def hash():
        return Hash()

    @staticmethod
    def now():
        now = datetime.datetime.now()
        return now.strftime("%Y-%d-%m %H:%M:%S.%f")

    @staticmethod
    def rea_now():
        return datetime.datetime.now()

    @staticmethod
    def find():
        return Find()

    @staticmethod
    def importlib():
        return importlib

    @staticmethod
    def crypt():
        crypt = Crypt
        return crypt

    @staticmethod
    def requests():
        return requests

    @staticmethod
    def request_nt_auth(username, password):
        return HttpNtlmAuth(username, password)

    @staticmethod
    def soap():
        return soap

    @staticmethod
    def save():
        return Save()

    @staticmethod
    def mail():
        return Mail

    @staticmethod
    def ldap():
        return ldap

    @staticmethod
    def ldap_mod_list():
        import ldap.modlist as mod_list
        return mod_list

    @staticmethod
    def template(**configs):
        return Template(**configs)

    @staticmethod
    def thread(**configs):
        return Thread(**configs)

    @staticmethod
    def jsonify_raw(raw_data):
        return jsonify(raw_data)

    @staticmethod
    def secure_filename(file_name):
        return secure_filename(file_name)
