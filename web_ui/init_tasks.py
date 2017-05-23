"""
Initial app tasks. This class is called in the manage.py file

"""
import envs
import json
import ast
import os
import db_controller
from nso_ui import settings


def add_data_to_db():
    DIR_PATH = os.path.dirname(os.path.realpath(__file__))  # Populate envs with configuration data
    with open(DIR_PATH + '/data/config.json') as data_file:
        json_dict = json.load(data_file)

        print "Saving device types in DB"

        for device_type in db_controller.get_device_types():
            device_type.delete()

        for item in json_dict['device_types']:
            db_controller.add_device_type(name=item['name'])

        print "Saving protocols in DB"
        for protocol in db_controller.get_protocols():
            protocol.delete()
        for item in json_dict['protocols']:
            db_controller.add_protocol(name=item['name'])
