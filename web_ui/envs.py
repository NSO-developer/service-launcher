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

Main access for environmental variables. The values in this file represent default values and can only be changed
using the config_files/config.json file. You will need to restart the app to apply those changes

"""

import os

__author__ = "Santiago Flores Kanter (sfloresk@cisco.com)"


def get_username():
    return os.getenv("USERNAME", "admin")


def get_password():
    return os.getenv("PASSWORD", "cisco123")


def get_nso_user():
    return os.getenv("NSO_USER", "admin")


def get_nso_password():
    return os.getenv("NSO_PASS", "admin")


def get_nso_ip():
    return os.getenv("NSO_IP", "")


def get_nso_netconf_port():
    return os.getenv("NSO_NETCONF_PORT", "")


def get_nso_rest_port():
    return os.getenv("NSO_REST_PORT", "")


def get_nso_server_user():
    """
    User from the linux server where NSO is running
    :return:
    """
    return os.getenv("NSO_SERVER_USER", "cisco")


def get_nso_server_password():
    """
    Password from the linux server where NSO is running
    :return:
    """
    return os.getenv("NSO_SERVER_PASSWORD", "cisco123")


def get_nso_packages_dir():
    """
    Password from the linux server where NSO is running
    :return:
    """
    return os.getenv("NSO_PACKAGES_DIR", "/home/cisco/ncs-run/packages")


def get_db_svc():
    return os.getenv("DB_SVC", "")


def get_db_port():
    return os.getenv("DB_PORT", "")


def get_db_name():
    return os.getenv("DB_NAME", "nso_ui")


def get_db_user():
    return os.getenv("DB_USER", "")


def get_db_password():
    return os.getenv("DB_PASSWORD", "")


def get_db_type():
    return os.getenv("DB_TYPE", "")
