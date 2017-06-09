#!/usr/bin/env python
import os
import sys
import json

if __name__ == "__main__":

    DIR_PATH = os.path.dirname(os.path.realpath(__file__))
    # Checks
    if not os.path.isdir(DIR_PATH + '/web_ui/data/'):
        raise Exception(DIR_PATH + "/web_ui/data folder is mandatory. Create the directory and restart")
    if not os.path.isfile(DIR_PATH + '/web_ui/data/config.json'):
        raise Exception(DIR_PATH +
                        "/web_ui/data/config.json file is mandatory. Create the file with the proper configuration and restart")

    """
        Populate envs with configuration data for the app
    """
    with open(DIR_PATH + '/web_ui/data/config.json') as data_file:
        json_dict = json.load(data_file)
        os.environ["USERNAME"] = json_dict['app']['user']
        os.environ["PASSWORD"] = json_dict['app']['password']
        os.environ["NSO_USER"] = json_dict['nso']['user']
        os.environ["NSO_PASS"] = json_dict['nso']['password']
        os.environ["NSO_IP"] = json_dict['nso']['ip']
        os.environ["NSO_NETCONF_PORT"] = json_dict['nso']['netconf_port']
        os.environ["NSO_REST_PORT"] = json_dict['nso']['rest_port']
        os.environ["NSO_SERVER_USER"] = json_dict['nso']['server']['user']
        os.environ["NSO_SERVER_PASSWORD"] = json_dict['nso']['server']['password']
        os.environ["NSO_PACKAGES_DIR"] = json_dict['nso']['server']['packages_dir']
        os.environ["DB_SVC"] = json_dict['db']['host']
        os.environ["DB_PORT"] = json_dict['db']['port']
        os.environ["DB_NAME"] = json_dict['db']['name']
        os.environ["DB_USER"] = json_dict['db']['user']
        os.environ["DB_PASSWORD"] = json_dict['db']['password']
        os.environ["DB_TYPE"] = json_dict['db']['type']

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nso_ui.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
    if sys.argv[1] == 'migrate':
        import web_ui.init_tasks

        web_ui.init_tasks.add_data_to_db()
