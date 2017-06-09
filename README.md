**Network Services Orchestrator Web User Interface**

This tool allows you to dynamically create and remove services from the web ui without coding. It syncs with the Network Services Orchestrator to dynamically generate the site.
If you add a new service to NSO, just go to Account -> Settings and press Re-Sync;  
After the process finishes, you will see your new service in the site.  

In addition, you can create and remove devices and see the alerts from NSO  


HTML user interface works better in Chrome and Firefox

Contacts:

* Santiago Flores ( sfloresk@cisco.com )

The app uses a configuration json file to set environment variables that are needed for the functionality that it provides.
The configuration file must be inside the /web_iu/data folder and the name must be config.json
If you change this file, you must restart the app
 It should have the following format:
```json
 {
  "device_types": [  
    {  
      "name": "cli"  
    },  
    {  
      "name": "netconf"  
    }  
  ],  
  "protocols": [  
    {  
      "name": "ssh"  
    },  
    {  
      "name": "telnet"  
    }  
  ],  
  "nso": {
    "user": "NSO USER",
    "password": "NSO PASSWORD - ASSUMES SAME PASSWORD FOR NETCONF AND RESTCONF APIs",
    "ip": "NSO URL or IP",
    "netconf_port": "NSO NETCONF PORT",
    "rest_port": "NSO REST PORT",
    "server": {
      "user": "SSH SERVER USER WHERE NSO IS RUNNING",
      "password": "SSH PASSWORD FOR ABOVE USER",
      "packages_dir": "NSO PACKAGE DIRECTORY"
    }
  },
  "app": {
    "comments": "Choose whatever you want, these are the login credentials for the app",
    "user": "APP USER",
    "password": "APP PASSWORD"
  },
  "db": {
    "comments": "Possible type options are sqlite or postgresql. If you use sqlite, the only value used is 'name'. You don't need to change the database name",
    "type": "MUST BE postgresql OR sqlite",
    "name": "nso_ui",
    "user": "DATABASE USER - ONLY USED FOR postgresql OPTION",
    "password": "DATABASE PASSWORD - ONLY USED FOR postgresql OPTION",
    "host": "DATABASE HOST - ONLY USED FOR postgresql OPTION",
    "port": "DATABASE PORT - ONLY USED FOR postgresql OPTION"
  }
}
```

**Container Installation**
You need to specify the configuration folder called data in this way:

docker run  --volume YOUR_PATH:/usr/src/app/web_ui/data -p YOUR_PORT:8025 sfloresk/nso-ui

The folder YOUR_PATH must have the config.json file in the format specified above


**Source Installation**

As this is a Django application you will need to either integrate the application in your production environment or you can
get it operational in a virtual environment on your computer/server. In the distribution is a requirements.txt file that you can
use to get the package requirements that are needed. The requirements file is located in the root directory of the distribution.

It might make sense for you to create a Python Virtual Environment before installing the requirements file. For information on utilizing
a virtual environment please read http://docs.python-guide.org/en/latest/dev/virtualenvs/. Once you have a virtual environment active then
install the packages in the requirements file.

`(virtualenv) % pip install -r requirements.txt
`

To run the the application execute in the root directory of the distribution:
 - python manage.py makemigrations
 - python manage.py migrate
 - python manage.py runserver 0.0.0.0:YOUR_PORT

**Known Issues**

Works with services that have been defined using leafs, leaf-lists and lists
The application's API token is hardcoded, it does not change in each login and there is not session timeout