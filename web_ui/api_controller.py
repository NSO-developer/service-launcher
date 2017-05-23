from __future__ import print_function  # This import is for python2.*
"""
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
"""
This class implements all external APIs calls. Help to have all external calls in a single file

"""

from ncclient import manager
from ncclientextensions.operations import SendCommand
from lxml import etree
from jinja2 import Environment
from jinja2 import FileSystemLoader
from xmltodict import parse
import requests
import os
import base64
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import pexpect
import sys
import shutil
import parser
import ast
import envs
import xmltodict
import db_controller

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class BaseAPI:
    """
    Base class for API clases
    """

    def __init__(self, user, password, ip, port):
        self.user = user
        self.password = password
        self.ip = ip
        self.port = port

    def check_credentials(self):
        pass


class ApiNetconf(BaseAPI):
    """
    Handler that manages the Netconf calls.

    """
    __author__ = 'Santiago Flores Kanter (sfloresk@cisco.com)'

    def __init__(self, user, password, ip, port):
        BaseAPI.__init__(self, user, password, ip, port)
        # Environment variable storing the physical location of netconf jinja templates
        self.env = Environment(loader=FileSystemLoader(DIR_PATH + '/netconf_templates'))

    def check_credentials(self):
        """
        Check if credentials are correct
        :return:
        """
        client_manager = None
        try:
            # Create a new manager with the given parameters
            client_manager = manager.connect(host=self.ip,
                                             port=int(self.port),
                                             username=self.user,
                                             password=self.password,
                                             hostkey_verify=False,
                                             device_params={},
                                             look_for_keys=False,
                                             allow_agent=False)
            return client_manager.connected
        except Exception as e:
            raise e
        finally:
            # Close NetConf connection if it has been established
            if client_manager is not None:
                if client_manager.connected:
                    client_manager.close_session()

    def send_edit_config_request(self, service_xml):
        """
        Send an edit config netconf
        :param service_xml: xml that specifies the changes in the configuration
        :return:
        """
        client_manager = None
        try:
            # Create a new rpc and manager with the given parameters
            client_manager, rpc_call = self.create_rpc_call()

            # Use the Jinja2 template provided to create the XML config
            template = self.env.get_template('edit_config.j2')
            rendered = template.render(service_xml=service_xml)

            # Do the request and save the response into a variable
            response = rpc_call.request(xml=etree.fromstring(rendered))
            return parse(str(response))

        except:
            raise
        finally:
            # Close NetConf connection if it has been established
            if client_manager is not None:
                if client_manager.connected:
                    client_manager.close_session()

    def send_get_config_request(self, filter_xml):
        """
        Send a get config request to the server
        :param filter_xml: xml that specifies the filter to be applied to the returned configuration
        :return:
        """
        client_manager = None
        try:
            # Create a new rpc and manager with the given parameters
            client_manager, rpc_call = self.create_rpc_call()

            # Use the Jinja2 template provided to create the XML config
            template = self.env.get_template('get_config.j2')
            rendered = template.render(filter_xml=filter_xml)

            # Do the request and save the response into a variable
            response = rpc_call.request(xml=etree.fromstring(rendered))
            return parse(str(response))
        except:
            raise
        finally:
            # Close NetConf connection if it has been established
            if client_manager is not None:
                if client_manager.connected:
                    client_manager.close_session()

    def create_rpc_call(self):
        """
        Create and send a remote procedure call
        :return:
        """
        # Create a new manager with the given parameters
        client_manager = manager.connect(host=self.ip,
                                         port=int(self.port),
                                         username=self.user,
                                         password=self.password,
                                         hostkey_verify=False,
                                         device_params={},
                                         look_for_keys=False,
                                         allow_agent=False)

        # Create a new SendCommand instance with the parameters of the NetConf client manager.
        rpc_call = SendCommand(client_manager._session,
                               device_handler=client_manager._device_handler,
                               async=client_manager._async_mode,
                               timeout=client_manager._timeout,
                               raise_mode=client_manager._raise_mode)
        # Increase the default timeout to 100 seconds
        rpc_call.timeout = 100
        return client_manager, rpc_call

    def create(self, template_service_name, **kwargs):
        """
        Create a configuration object
        :param template_service_name: jinja template to be used
        :param kwargs: arguments to be replaced in the jinja template
        :return:
        """
        template = self.env.get_template(template_service_name + '.j2')
        rendered = template.render(**kwargs)
        self.send_edit_config_request(rendered)

    def delete(self, template_service_name, **kwargs):
        """
        Delete a configuration object
        :param template_service_name: jinja tempalte to be used
        :param kwargs: arguments to be replaced in the jinja template
        :return:
        """
        template = self.env.get_template(template_service_name + '.j2')
        rendered = template.render(operation='delete', **kwargs)
        self.send_edit_config_request(rendered)

    def get_config(self, template_filter_name, **kwargs):
        """
        Return configurations of the netconf device
        :param template_filter_name: jinja template with filter to be applied to the returned configuration
        :param kwargs: arguments to be replaced in the jinja template
        :return:
        """
        template = self.env.get_template(template_filter_name + '.j2')
        rendered = template.render(**kwargs)
        return self.send_get_config_request(rendered)

    def edit_config(self, template_name, **kwargs):
        """
        Send edit config to netconf server
        :param template_name: edit config jinja template to be used
        :param kwargs: arguments to be replaced in the jinja template
        :return:
        """
        template = self.env.get_template(template_name + '.j2')
        rendered = template.render(**kwargs)
        return self.send_edit_config_request(rendered)


class APINetconfNso(ApiNetconf):
    def get_devices(self):
        """
        Return devices managed by NSO
        :return:
        ast.literal_eval(
            json.dumps(xmltodict.parse(str(response))['rpc-reply']['data'], ensure_ascii=False).replace("null",
                                                                                                        '"None"'))

        """

        # Get the devices using get config call
        result = self.get_config('nso/get_devices_filter')

        json_string = json.dumps(
            result['rpc-reply']['data']['devices']['device'],
            ensure_ascii=False).replace("null", '"None"')
        json_dict = ast.literal_eval(json_string)
        if not isinstance(json_dict, type([])):
            result.append(json_dict)
        else:
            result = json_dict
        return result

    def send_service(self, service_xml):
        self.send_edit_config_request(service_xml)

    def delete_service(self, **kwargs):
        self.edit_config('nso/delete_service', **kwargs)

    def add_device(self, name, device_type, ip, port, authgroup, protocol=None, ned_id=None, ned_xmlns=None):
        self.edit_config('nso/device',
                         name=name,
                         device_type=device_type,
                         ip=ip,
                         authgroup=authgroup,
                         protocol=protocol,
                         ned_id=ned_id,
                         ned_xmlns=ned_xmlns,
                         port=port)

    def delete_device(self, name):
        self.delete('nso/device', name=name)


class ApiRestNSO(BaseAPI):
    """
        Handler that manages the REST calls to NSO.

        """
    __author__ = 'Santiago Flores Kanter (sfloresk@cisco.com)'

    def __init__(self, user, password, ip, port):
        BaseAPI.__init__(self, user, password, ip, port)

    def get_headers(self):
        """
        Get the headers needed to do http rest calls
        :return:
        """
        headers = {
            'authorization': "Basic " + base64.b64encode(self.user + ':' + self.password),
            'content-type': "application/vnd.yang.operation+json"
        }
        return headers

    def check_credentials(self):
        """
        Check if credentials are valid
        :return:
        """
        try:
            # Create a new request with the given parameters
            response = requests.get('http://' + self.ip + ':' + self.port + '/api/running/devices/',
                                    headers=self.get_headers())
        except Exception as e:
            raise e
        return 199 < response.status_code < 400

    def fetch_ssh_keys(self):
        """
        Fetch ssh keys with all devices three times in case of failures
        :return:
        """
        tries = 3
        payload = ''
        while tries > 0:
            # Create a new request with the given parameters
            response = requests.post(
                'http://' + self.ip + ':' + self.port + '/api/running/devices/_operations/fetch-ssh-host-keys',
                headers=self.get_headers())
            payload = json.loads(response.text)
            tries -= 1
        return payload

    def sync_from_devices(self):
        """
        Sync database from all devices three times in case of failures
        :return:
        """
        tries = 3
        payload = ''
        while tries > 0:
            # Create a new request with the given parameters
            response = requests.post(
                'http://' + self.ip + ':' + self.port + '/api/running/devices/_operations/sync-from',
                headers=self.get_headers())
            payload = json.loads(response.text)
            tries -= 1
        return payload

    def get_running_services(self, service_name):
        result = []
        response = requests.get(
            'http://' + self.ip + ':' + self.port + '/api/running/services/' + service_name,
            headers=self.get_headers())
        if 199 < response.status_code < 400:
            if response.text != '':
                xml_dict = xmltodict.parse(response.text)
                json_string = json.dumps(xml_dict, ensure_ascii=False)
                json_dict = ast.literal_eval(json_string.replace('@', ''))['collection'][service_name]
                if not isinstance(json_dict, type([])):
                    json_dict['type'] = service_name
                    result.append(json_dict)
                else:
                    for service in json_dict:
                        service['type'] = service_name
                    result = json_dict
        return result

    def get_alerts(self):
        result = []
        response = requests.get(
            'http://' + self.ip + ':' + self.port + '/api/operational/alarms/alarm-list',
            headers=self.get_headers())
        if 199 < response.status_code < 400:
            if response.text != '':
                xml_dict = xmltodict.parse(response.text)
                json_string = json.dumps(xml_dict, ensure_ascii=False)
                json_dict = ast.literal_eval(json_string.replace('null', '"None"').replace('\'', ''))
                if 'alarm-list' in json_dict.keys():
                    if 'alarm' in json_dict['alarm-list'].keys():
                        if not isinstance(json_dict['alarm-list']['alarm'], type([])):
                            result.append(json_dict['alarm-list']['alarm'])
                        else:
                            result = json_dict['alarm-list']['alarm']
        return result


class ApiPackagesNSO(BaseAPI):
    """
    Since there is no way to get the packages installed in NSO, a new class has been created to do the following:
    - Get service yang files from NSO server
    - Parse those files to json
    - Store a cache in yang_templates/nso_service_templates
    - Refresh the cache when needed
    """

    def __init__(self, user, password, ip):
        BaseAPI.__init__(self, user, password, ip, port=None)
        self.pexpect_time_out = 2
        self.package_dir = "/data/packages/"
        self.service_templates_dir = "/data/service_templates"
        self.tmp_web_ui_packages_dir = "/tmp/web_ui_packages/"
        self.nso_data_dir = "/data"

    def get_packages(self):
        # Remove cache
        if os.path.isdir(DIR_PATH + self.package_dir):
            shutil.rmtree(DIR_PATH + self.package_dir)
        if os.path.isdir(DIR_PATH + self.service_templates_dir):
            shutil.rmtree(DIR_PATH + self.service_templates_dir)

        # Recreate needed directories
        os.mkdir(DIR_PATH + self.service_templates_dir)

        # Copy the files of interest in a tmp file on remote server
        command = "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null " \
                  + self.user + "@nso.lwr04.cisco.com"
        ssh_pexpect = pexpect.spawn(command=command)
        ssh_pexpect.logfile = sys.stdout

        try:
            ssh_pexpect.expect('[Pp]assword:', self.pexpect_time_out)
            ssh_pexpect.sendline(self.password)
            ssh_pexpect.expect('[#$]', self.pexpect_time_out)
            ssh_pexpect.sendline('rm -rf ' + self.tmp_web_ui_packages_dir)
            ssh_pexpect.expect('[#$]', self.pexpect_time_out)
            ssh_pexpect.sendline('mkdir ' + self.tmp_web_ui_packages_dir)
            ssh_pexpect.expect('[#$]', self.pexpect_time_out)
            ssh_pexpect.sendline(
                "rsync -zarv --copy-links --include '*/' --include '*.yang' --exclude '*' "
                + envs.get_nso_packages_dir() + " " + self.tmp_web_ui_packages_dir)
            ssh_pexpect.expect('[#$]', 100)
        except:
            raise
        finally:
            ssh_pexpect.close()

        # Copy files to local directory
        command = "scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -r " \
                  + self.user + "@nso.lwr04.cisco.com:" + self.tmp_web_ui_packages_dir + "/packages " \
                  + DIR_PATH + self.nso_data_dir
        ssh_pexpect = pexpect.spawn(command=command)
        ssh_pexpect.logfile = sys.stdout

        try:
            ssh_pexpect.expect('[Pp]assword:', self.pexpect_time_out)
            ssh_pexpect.sendline(self.password)
            ssh_pexpect.expect(pexpect.EOF, 1000)
        except:
            raise
        finally:
            ssh_pexpect.close()

        # Parse yang packages to xml and json
        for package_dir in os.listdir(DIR_PATH + self.package_dir):
            print("Found package " + package_dir + ".")
            is_package_supported = False
            for yang_file in os.listdir(DIR_PATH + self.package_dir + '/' + package_dir + '/src/yang'):
                xml_data = parser.yang_to_xml(
                    src=DIR_PATH + self.package_dir + '/' + package_dir + '/src/yang/' + yang_file)
                json_data = parser.xml_to_json(xml_data)
                dict_data = ast.literal_eval(json_data.replace('null', '"None"').replace('@', ''))

                if "module" in dict_data.keys():
                    if "namespace" in dict_data['module'].keys():
                        # Services
                        if "augment" in dict_data['module']:
                            if "target-node" in dict_data['module']['augment']:
                                if dict_data['module']['augment']['target-node'] == "/ncs:services":
                                    if len(os.listdir(
                                                                            DIR_PATH + self.package_dir + '/' + package_dir + '/src/yang')) == 1:
                                        print("Package " + package_dir + " is a service. Adding it to service catalog")
                                        parser.yang_to_xml(
                                            src=DIR_PATH + self.package_dir + '/' + package_dir + '/src/yang/' + yang_file,
                                            dest=DIR_PATH + self.service_templates_dir + '/' + yang_file + '.xml')
                                        is_package_supported = True
                                    else:
                                        print("Package " + package_dir +
                                              " has more than one file in its yang definition. Not supported")
                                    break
                        # NEDs
                        elif "uri" in dict_data['module']["namespace"].keys():
                            if '/ned/' in dict_data['module']["namespace"]["uri"]:
                                if "identity" in dict_data['module'].keys():
                                    if "prefix" in dict_data['module'].keys():
                                        ned_prefix = dict_data['module']['prefix']["value"]
                                        ned_name = dict_data['module']['identity']["name"]
                                        ned_xmlns = ned_prefix + '="' + dict_data['module']['namespace']["uri"] + '"'

                                        print("Package " + package_dir +
                                              " is a NED. Adding it to NED database with these options:")
                                        print("NED ID: " + ned_prefix + ':' + ned_name)
                                        print("NED prefix: " + ned_prefix)
                                        print("NED name: " + ned_name)
                                        print("NED xmlns: " + ned_xmlns)
                                        db_controller.add_ned(ned_id=ned_prefix + ':' + ned_name,
                                                              prefix=ned_prefix,
                                                              name=ned_name,
                                                              xmlns=ned_xmlns)
                                        is_package_supported = True
                                        break
            if not is_package_supported:
                print("Sorry, package " + package_dir + " is not supported")

        return self.get_services_cache()

    def get_services_cache(self):
        """
        Return service definitions under data/service_templates
        :return:
        """
        result = []
        if os.path.isdir(DIR_PATH + self.package_dir):
            for svc_file in os.listdir(DIR_PATH + self.service_templates_dir):
                if svc_file.endswith('.xml'):
                    json_data = parser.xml_file_to_json(src=DIR_PATH + self.service_templates_dir + '/' + svc_file)
                    result.append(ast.literal_eval(json_data.replace('null', '"None"').replace('@', '')))
                    # Save file for debugging purposes
                    parser.xml_file_to_json(src=DIR_PATH + self.service_templates_dir + '/' + svc_file,
                                            dest=DIR_PATH + self.service_templates_dir + '/' + svc_file + '.json')

        return result
