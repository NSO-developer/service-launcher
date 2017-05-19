"""

Main store for environmental variables
This are the parameters that can be changed for the application

"""

import os

__author__ = "Santiago Flores Kanter (sfloresk@cisco.com)"


def get_username():
    return os.getenv("USERNAME", "admin")


def get_password():
    return os.getenv("PASSWORD", "C1sc0123")


def get_nso_user():
    return os.getenv("NSO_USER", "admin")


def get_nso_password():
    return os.getenv("NSO_PASS", "admin")


def get_nso_ip():
    return os.getenv("NSO_IP", "nso.lwr04.cisco.com")


def get_nso_netconf_port():
    return os.getenv("NSO_PORT", "2022")


def get_nso_rest_port():
    return os.getenv("NSO_PORT", "8080")


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
    return os.getenv("NSO_SERVER_PASSWORD", "C1sc0123")

def get_nso_packages_dir():
    """
    Password from the linux server where NSO is running
    :return:
    """
    return os.getenv("NSO_PACKAGES_DIR", "/home/cisco/ncs-run/packages")



def get_db_svc():
    return os.getenv("DB_SVC", "oce-master.lwr04.cisco.com")


def get_db_port():
    return os.getenv("DB_PORT", "30005")


def get_db_name():
    return os.getenv("DB_NAME", "nso_ui")


def get_db_user():
    return os.getenv("DB_USER", "postgres")


def get_db_password():
    return os.getenv("DB_PASSWORD", "C1sc0123")
