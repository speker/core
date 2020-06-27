# import time
#
# from core.utilities.tcp.json.json_client import JsonClient
#
# client = JsonClient().get_instance()
# client.connect('127.0.0.1', 5000)
#
# # token='$2b$12$q6YA//gan42.AKZeLt8sNOdefb58BxUlh8T7.CPJAH1CHdkaU03oi'
# # client.send_obj({"token": token, "method": "check_integrator_token",
# #                  "data": {"integrator_token": token}})
# client.send_obj({"integrator_id": "d65457cf-fa91-46dd-89bf-e75f7a416005",
#                  "integrator_secret": "3ad2dda3-30cd-48ab-ab7b-07f8cd69f630",
#                  })
# reader = client.read_obj()
# print(reader)
#
# if reader['data']['success'] is True:
#     token = reader['data']['payload']['token']
#     print(token)
#     # client.send_obj({"token": token, "method": "check_integrator_token",
#     #                  "data": {"integrator_token": token}})
#     client.send_obj({"token": token, "method": "user_login",
#                      "data": {"username": "admin", "password": "ReActor2019!!..", "token_type": "bearer"}})
#     reader2 = client.read_obj()
#
#     print(reader2)
#     # if reader2['data']['success'] is True:
#     #     # time.sleep(20)
#     #     token = reader['data']['payload']['token']
#     #     user_token = reader2['data']['payload']['user_token']
#     #     client.send_obj({"token": token, "method": "check_user_token",
#     #                      "data": {"user_token": user_token}})
#     #     readers = client.read_obj()
#     #     print(readers)
#     # else:
#     #     print(reader)
import datetime

from core.utilities.rest import jsonify

import datetime
from core.reapy import ReaPy

try:
    use_mediation = ReaPy.configuration().get_configuration()['system']['use_mediation']
    if use_mediation is True:
        from core.mediation_model import MediationModel as Model
    else:
        from core.model import Model
except ImportError:
    from core.model import Model

    query = Model(ReaPy.get_reactor_source('yeten')).update('paydas', {
        'SET': {'guncelleme_tarihi': str(datetime.datetime.now())},
        'CONDITION': {
            0: {'col': 'paydas_id', 'operator': '=',
                'value': 'b3f67bc8-ded0-4d2a-b662-08e732e59396'
                }}}).data()
print(query)
