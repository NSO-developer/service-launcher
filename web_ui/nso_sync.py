"""
Initial config for the application

"""

import db_controller
from api_controller import ApiPackagesNSO
import envs
import json
import os
def sync():
    DIR_PATH = os.path.dirname(os.path.realpath(__file__))

    print "Getting package definitions from NSO:"
    nso_packages_controller = ApiPackagesNSO(envs.get_nso_server_user(), envs.get_nso_server_password(),
                                             envs.get_nso_ip())

    for ned in db_controller.get_neds():
        ned.delete()

    data = nso_packages_controller.get_packages()

    print "Services loaded:"
    print data

    print "Saving device types in DB"

    for device_type in db_controller.get_device_types():
        device_type.delete()

    with open(DIR_PATH + '/device_types/device_types.json') as data_file:
        json_data = json.load(data_file)

        for item in json_data:
            db_controller.add_device_type(name=item['name'])

    print "Saving protocols in DB"
    for protocol in db_controller.get_protocols():
        protocol.delete()
    with open(DIR_PATH + '/protocols/protocols.json') as data_file:
        json_data = json.load(data_file)
        for item in json_data:
            db_controller.add_protocol(name=item['name'])
