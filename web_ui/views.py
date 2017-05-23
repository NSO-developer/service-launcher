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
from django.shortcuts import render, redirect
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from authentication import get_token, is_token_valid
import os
from jinja2 import Environment
from jinja2 import FileSystemLoader
import traceback
from api_controller import APINetconfNso, ApiRestNSO, ApiPackagesNSO
import envs
import threading
import parser
import db_controller
import models

import nso_sync

""" Utils """

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
JSON_TEMPLATES_PATH = Environment(loader=FileSystemLoader(DIR_PATH + '/json_templates'))


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


""" HTML Templates """


def login(request):
    if 'token' in request.session.keys():
        if is_token_valid(request.session['token']):
            return redirect('index')

    return render(request, 'web_app/login.html')


def logout(request):
    if 'token' in request.session.keys():
        request.session.pop('token')
    return redirect('login')


def index(request):
    if 'token' in request.session.keys():
        if is_token_valid(request.session['token']):
            return render(request, 'web_app/index.html')

    return redirect('login')


def home(request):
    if 'token' in request.session.keys():
        if is_token_valid(request.session['token']):
            return render(request, 'web_app/home.html')

    return redirect('login')


def dashboard(request):
    if 'token' in request.session.keys():
        if is_token_valid(request.session['token']):
            return render(request, 'web_app/dashboard.html')

    return redirect('login')


def list_services(request):
    if 'token' in request.session.keys():
        if is_token_valid(request.session['token']):
            return render(request, 'web_app/services/list_service_catalog.html')

    return redirect('login')


def service(request, service_name):
    if 'token' in request.session.keys():
        if is_token_valid(request.session['token']):
            return render(request, 'web_app/services/service_catalog.html')

    return redirect('login')


def list_running_services(request):
    if 'token' in request.session.keys():
        if is_token_valid(request.session['token']):
            return render(request, 'web_app/services/list_service_running.html')

    return redirect('login')


def list_devices(request):
    if 'token' in request.session.keys():
        if is_token_valid(request.session['token']):
            return render(request, 'web_app/devices/list_devices.html')

    return redirect('login')


def add_device(request):
    if 'token' in request.session.keys():
        if is_token_valid(request.session['token']):
            return render(request, 'web_app/devices/add_device.html')

    return redirect('login')


def list_alerts(request):
    if 'token' in request.session.keys():
        if is_token_valid(request.session['token']):
            return render(request, 'web_app/alerts/list_alert.html')

    return redirect('login')


def settings(request):
    if 'token' in request.session.keys():
        if is_token_valid(request.session['token']):
            return render(request, 'web_app/settings/settings.html')

    return redirect('login')


""" APIs """


@csrf_exempt
def api_login(request):
    """
    POST:
        Generates and return a new token. Stores that token in a session variable as well
    :param request:
    :return:
    """
    if request.method == 'POST':
        payload = json.loads(request.body)
        token = get_token(payload['username'], payload['password'])
        if token:
            request.session['token'] = token
            response_data = {'token': token}
            return JSONResponse(response_data)
        else:
            return JSONResponse("Wrong credentials", status=401)


@csrf_exempt
def api_token(request):
    """
    GET:
        Return the token stored in the session cookie
    :param request:
    :return:
    """
    if request.method == 'GET':
        if 'token' in request.session.keys():
            return JSONResponse({'token': request.session['token']})
        else:
            return JSONResponse("User not logged", status=401)
    else:
        return JSONResponse("Bad request. " + request.method + " is not supported", status=400)


@csrf_exempt
def api_devices(request):
    """
        POST:
            Add device to NSO
        GET:
            List all devices in NSO
        :param request:
        :return:
        """
    # Check credentials
    if 'HTTP_AUTHORIZATION' in request.META:
        if is_token_valid(request.META['HTTP_AUTHORIZATION'].split(' ')[1]):
            if request.method == 'POST':
                print "*** Adding New Device to NSO ***"
                try:
                    payload = json.loads(request.body)

                    # Create NSO controller
                    netconf_controller = APINetconfNso(envs.get_nso_user(), envs.get_nso_password(), envs.get_nso_ip(),
                                                       envs.get_nso_netconf_port())

                    # Required parameters
                    name = payload['name']
                    device_type = payload['device_type']
                    ip = payload['ip']
                    authgroup = payload['authgroup']
                    port = payload['port']

                    # Optionals
                    protocol = None
                    ned_id = None
                    ned = models.NED(xmlns='')

                    if payload['device_type'] == 'cli':
                        protocol = payload['protocol']
                        ned_id = payload['ned_id']
                        ned = db_controller.get_first_ned(ned_id=payload['ned_id'])

                    netconf_controller.add_device(name=name,
                                                  device_type=device_type,
                                                  ip=ip,
                                                  authgroup=authgroup,
                                                  protocol=protocol,
                                                  ned_id=ned_id,
                                                  ned_xmlns=ned.xmlns,
                                                  port=port)

                    rest_controller = ApiRestNSO(envs.get_nso_user(), envs.get_nso_password(), envs.get_nso_ip(),
                                                 envs.get_nso_rest_port())

                    # Fetch keys
                    rest_controller.fetch_ssh_keys()

                    # Sync configuration
                    rest_controller.sync_from_devices()

                    return JSONResponse('Ok')

                except Exception as e:
                    print traceback.print_exc()
                    return JSONResponse({'error': e.__class__.__name__, 'message': str(e)}, status=500)

            elif request.method == 'GET':
                try:
                    # Create a new api controller
                    nso_controller = APINetconfNso(envs.get_nso_user(), envs.get_nso_password(), envs.get_nso_ip(),
                                                   envs.get_nso_netconf_port())

                    data = nso_controller.get_devices()

                    return JSONResponse(data)
                except Exception as e:
                    print traceback.print_exc()
                    # return the error to web client
                    return JSONResponse({'error': e.__class__.__name__, 'message': str(e)}, status=500)

            else:
                return JSONResponse("Bad request. " + request.method + " is not supported", status=400)
        else:
            return JSONResponse("Invalid Token", status=401)
    else:
        return JSONResponse("Bad request. HTTP_AUTHORIZATION header is required", status=400)


@csrf_exempt
def api_delete_devices(request):
    """
        POST:
            Delete device from NSO
        :param request:
        :return:
        """
    # Check credentials
    if 'HTTP_AUTHORIZATION' in request.META:
        if is_token_valid(request.META['HTTP_AUTHORIZATION'].split(' ')[1]):
            if request.method == 'POST':
                print "*** Delete device from NSO ***"
                try:
                    payload = json.loads(request.body)

                    controller = APINetconfNso(envs.get_nso_user(), envs.get_nso_password(), envs.get_nso_ip(),
                                               envs.get_nso_netconf_port())
                    controller.delete_device(name=payload['name'])

                    return JSONResponse('Ok')

                except Exception as e:
                    print traceback.print_exc()
                    return JSONResponse({'error': e.__class__.__name__, 'message': str(e)}, status=500)
            else:
                return JSONResponse("Bad request. " + request.method + " is not supported", status=400)
        else:
            return JSONResponse("Invalid Token", status=401)
    else:
        return JSONResponse("Bad request. HTTP_AUTHORIZATION header is required", status=400)


@csrf_exempt
def api_services(request):
    """
        GET:
            List all cache services from NSO
        POST:
            Refresh cache getting all services from NSO
        :param request:
        :return:
        """
    # Check credentials
    if 'HTTP_AUTHORIZATION' in request.META:
        if is_token_valid(request.META['HTTP_AUTHORIZATION'].split(' ')[1]):
            if request.method == 'GET':
                try:
                    # Create a new api controller
                    nso_packages_controller = ApiPackagesNSO(envs.get_nso_server_user(), envs.get_nso_server_password(),
                                                             envs.get_nso_ip())

                    nso_services = nso_packages_controller.get_services_cache()

                    return JSONResponse(nso_services)
                except Exception as e:
                    print traceback.print_exc()
                    # return the error to web client
                    return JSONResponse({'error': e.__class__.__name__, 'message': str(e)}, status=500)

            elif request.method == 'POST':
                try:
                    for thread in threading.enumerate():
                        if thread.name == 'NSO_sync':
                            if thread.isAlive():
                                return JSONResponse('Sync is in process')
                    print "*** Launching daemon to refresh NSO data Cache ***"
                    threading.Thread(
                        name=str("NSO_sync"),
                        target=nso_sync.sync
                    ).start()
                    return JSONResponse('ok')
                except Exception as e:
                    print traceback.print_exc()
                    # return the error to web client
                    return JSONResponse({'error': e.__class__.__name__, 'message': str(e)}, status=500)

            else:
                return JSONResponse("Bad request. " + request.method + " is not supported", status=400)

        else:
            return JSONResponse("Invalid Token", status=401)
    else:
        return JSONResponse("Bad request. HTTP_AUTHORIZATION header is required", status=400)


@csrf_exempt
def api_running_services(request, ):
    """
        GET:
            List all running services from NSO
        POST:
            Creates a new service
    :param request:
    :return:
    """
    # Check credentials
    if 'HTTP_AUTHORIZATION' in request.META:
        if is_token_valid(request.META['HTTP_AUTHORIZATION'].split(' ')[1]):
            if request.method == 'GET':
                try:

                    # Create a new api controller
                    nso_packages_controller = ApiPackagesNSO(envs.get_nso_server_user(), envs.get_nso_server_password(),
                                                             envs.get_nso_ip())

                    # Get Services definition

                    nso_services = nso_packages_controller.get_services_cache()

                    # Create a new netconf nso controller
                    nso_controller = ApiRestNSO(user=envs.get_nso_user(),
                                                password=envs.get_nso_password(),
                                                ip=envs.get_nso_ip(),
                                                port=envs.get_nso_rest_port())
                    nso_running_services = []
                    # Assembly response
                    for service_definition in nso_services:
                        running_services = nso_controller.get_running_services(
                            service_name=service_definition['module']['name'])
                        for running_service in running_services:
                            running_service['service_key'] = service_definition['module']['augment']['list']['key'][
                                'value']
                        nso_running_services.append({
                            'data': running_services,
                            'name': service_definition['module']['name']
                        })

                    return JSONResponse(nso_running_services)
                except Exception as e:
                    print traceback.print_exc()
                    # return the error to web client
                    return JSONResponse({'error': e.__class__.__name__, 'message': str(e)}, status=500)

            elif request.method == 'POST':
                try:
                    # Parse the json service
                    payload = json.loads(request.body)

                    # Create a new netconf nso controller
                    nso_controller = APINetconfNso(user=envs.get_nso_user(),
                                                   password=envs.get_nso_password(),
                                                   ip=envs.get_nso_ip(),
                                                   port=envs.get_nso_netconf_port())

                    # Creates the xml from the request payload
                    service_xml = parser.json_to_nso_service_xml(payload)

                    # Send service request to NSO
                    nso_controller.send_service(service_xml)

                    return JSONResponse('ok')
                except Exception as e:
                    print traceback.print_exc()
                    # return the error to web client
                    return JSONResponse({'error': e.__class__.__name__, 'message': str(e)}, status=500)

            else:
                return JSONResponse("Bad request. " + request.method + " is not supported", status=400)

        else:
            return JSONResponse("Invalid Token", status=401)
    else:
        return JSONResponse("Bad request. HTTP_AUTHORIZATION header is required", status=400)


@csrf_exempt
def api_delete_running_services(request):
    """
        POST:
            Delete a service
    :param request:
    :return:
    """
    # Check credentials
    if 'HTTP_AUTHORIZATION' in request.META:
        if is_token_valid(request.META['HTTP_AUTHORIZATION'].split(' ')[1]):
            if request.method == 'POST':
                try:
                    # Parse the json
                    payload = json.loads(request.body)
                    # Create a new netconf nso controller
                    nso_controller = APINetconfNso(user=envs.get_nso_user(),
                                                   password=envs.get_nso_password(),
                                                   ip=envs.get_nso_ip(),
                                                   port=envs.get_nso_netconf_port())

                    # Send service request to NSO
                    nso_controller.delete_service(type=payload['type'],
                                                  xmlns=payload['xmlns'],
                                                  name=payload[payload['service_key']],
                                                  key=payload['service_key'])

                    return JSONResponse('ok')
                except Exception as e:
                    print traceback.print_exc()
                    # return the error to web client
                    return JSONResponse({'error': e.__class__.__name__, 'message': str(e)}, status=500)
        else:
            return JSONResponse("Invalid Token", status=401)
    else:
        return JSONResponse("Bad request. HTTP_AUTHORIZATION header is required", status=400)


@csrf_exempt
def api_protocols(request):
    """
    GET:
        List all supported protocols
    :param request:
    :return:
    """
    # Check credentials
    if 'HTTP_AUTHORIZATION' in request.META:
        if is_token_valid(request.META['HTTP_AUTHORIZATION'].split(' ')[1]):
            if request.method == 'GET':
                cli_protocols = []
                for protocol in db_controller.get_protocols():
                    cli_protocols.append({
                        'name': protocol.name,
                        'id': protocol.id
                    })
                return JSONResponse(cli_protocols)
            else:
                return JSONResponse("Bad request. " + request.method + " is not supported", status=400)
        else:
            return JSONResponse("Invalid Token", status=401)
    else:
        return JSONResponse("Bad request. HTTP_AUTHORIZATION header is required", status=400)


@csrf_exempt
def api_device_types(request):
    """
        GET:
            List all supported device types
        :param request:
        :return:
        """
    # Check credentials
    if 'HTTP_AUTHORIZATION' in request.META:
        if is_token_valid(request.META['HTTP_AUTHORIZATION'].split(' ')[1]):
            if request.method == 'GET':
                device_types = []
                for device_type in db_controller.get_device_types():
                    device_types.append({
                        'id': device_type.id,
                        'name': device_type.name
                    })
                return JSONResponse(device_types)
            else:
                return JSONResponse("Bad request. " + request.method + " is not supported", status=400)
        else:
            return JSONResponse("Invalid Token", status=401)
    else:
        return JSONResponse("Bad request. HTTP_AUTHORIZATION header is required", status=400)


@csrf_exempt
def api_authgroups(request):
    """
            GET:
                List all authgroups from NSO
            :param request:
            :return:
            """
    # Check credentials
    if 'HTTP_AUTHORIZATION' in request.META:
        if is_token_valid(request.META['HTTP_AUTHORIZATION'].split(' ')[1]):
            if request.method == 'GET':
                try:
                    controller = APINetconfNso(envs.get_nso_user(), envs.get_nso_password(), envs.get_nso_ip(),
                                               envs.get_nso_netconf_port())
                    result = controller.get_config('nso/get_authgroup_filter')
                    response_data = []
                    for authgroup in result['rpc-reply']['data']['devices']['authgroups']['group']:
                        response_data.append({
                            'name': authgroup['name']
                        })
                    return JSONResponse(response_data)
                except Exception as e:
                    return JSONResponse({'error': e.__class__.__name__, 'message': str(e)}, status=500)
            else:
                return JSONResponse("Bad request. " + request.method + " is not supported", status=400)
        else:
            return JSONResponse("Invalid Token", status=401)
    else:
        return JSONResponse("Bad request. HTTP_AUTHORIZATION header is required", status=400)


@csrf_exempt
def api_neds(request):
    """
        GET:
            List all supported Network Element Drivers
        :param request:
        :return:
        """
    # Check credentials
    if 'HTTP_AUTHORIZATION' in request.META:
        if is_token_valid(request.META['HTTP_AUTHORIZATION'].split(' ')[1]):
            if request.method == 'GET':
                neds = []
                for ned in db_controller.get_neds():
                    neds.append({
                        'id': ned.ned_id,
                        'name': ned.name
                    })
                return JSONResponse(neds)
            else:
                return JSONResponse("Bad request. " + request.method + " is not supported", status=400)
        else:
            return JSONResponse("Invalid Token", status=401)
    else:
        return JSONResponse("Bad request. HTTP_AUTHORIZATION header is required", status=400)


@csrf_exempt
def api_alerts(request):
    """
    GET:
        List all alerts in NSO
    :param request:
    :return:
    """
    # Check credentials
    if 'HTTP_AUTHORIZATION' in request.META:
        if is_token_valid(request.META['HTTP_AUTHORIZATION'].split(' ')[1]):
            if request.method == 'GET':
                rest_controller = ApiRestNSO(envs.get_nso_user(), envs.get_nso_password(), envs.get_nso_ip(),
                                             envs.get_nso_rest_port())
                alarms = rest_controller.get_alerts()

                # Fetch keys
                return JSONResponse(alarms)
            else:
                return JSONResponse("Bad request. " + request.method + " is not supported", status=400)
        else:
            return JSONResponse("Invalid Token", status=401)
    else:
        return JSONResponse("Bad request. HTTP_AUTHORIZATION header is required", status=400)


@csrf_exempt
def api_settings(request):
    """
    GET:
        List all alerts in NSO
    :param request:
    :return:
    """
    # Check credentials
    if 'HTTP_AUTHORIZATION' in request.META:
        if is_token_valid(request.META['HTTP_AUTHORIZATION'].split(' ')[1]):
            if request.method == 'GET':

                settings = {}
                sync_state = 'in_sync'
                # Check if is syncing
                for thread in threading.enumerate():
                    if thread.name == 'NSO_sync':
                        if thread.isAlive():
                            sync_state = 'performing_sync'

                settings['nso'] = {
                    'address': envs.get_nso_ip(),
                    'http_port': envs.get_nso_rest_port(),
                    'netconf_port': envs.get_nso_netconf_port(),
                    'package_directory': envs.get_nso_packages_dir(),
                    'sync_state': sync_state
                }
                # Fetch keys
                return JSONResponse(settings)
            else:
                return JSONResponse("Bad request. " + request.method + " is not supported", status=400)
        else:
            return JSONResponse("Invalid Token", status=401)
    else:
        return JSONResponse("Bad request. HTTP_AUTHORIZATION header is required", status=400)
