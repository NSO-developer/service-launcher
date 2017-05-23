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
URL mapping of the application
"""

from django.conf.urls import url

from . import views

urlpatterns = [

    # Angular URL mappings
    url(r'^home/?$', views.index, name='home'),
    url(r'^ng/home/?$', views.home, name='home'),

    url(r'^dashboard/?$', views.index, name='dashboard'),
    url(r'^ng/dashboard/?$', views.dashboard, name='dashboard'),

    url(r'^catalog/services/new/[\w.@+-]+/?$', views.index, name='service'),
    url(r'^ng/catalog/services/new/(?P<service_name>[\w.@+-]+)/?$', views.service, name='service'),

    url(r'^catalog/services/?$', views.index, name='list_services'),
    url(r'^ng/catalog/services/?$', views.list_services, name='list_services'),

    url(r'^running/services/?$', views.index, name='list_services'),
    url(r'^ng/running/services/?$', views.list_running_services, name='list_services'),

    url(r'^devices/?$', views.index, name='list_devices'),
    url(r'^ng/devices/?$', views.list_devices, name='list_devices'),

    url(r'^devices/new/?$', views.index, name='list_devices'),
    url(r'^ng/devices/new/?$', views.add_device, name='add_device'),

    url(r'^alerts/?$', views.index, name='list_alerts'),
    url(r'^ng/alerts/?$', views.list_alerts, name='list_alerts'),

    url(r'^settings/?$', views.index, name='list_alerts'),
    url(r'^ng/settings/?$', views.settings, name='list_alerts'),

    # Basic URL mappings
    url(r'^$', views.index, name='index'),
    url(r'^login/?$', views.login, name='login'),
    url(r'^logout/?$', views.logout, name='logout'),
    url(r'^index/?$', views.index, name='index'),

    # API URLs

    # Authentication
    url(r'^api/login/?$', views.api_login, name='api_login'),
    url(r'^api/token/?$', views.api_token, name='api_token'),

    # Services
    url(r'^api/catalog/services/?$', views.api_services, name='api_services'),
    url(r'^api/running/services/?$', views.api_running_services, name='api_running_services'),
    url(r'^api/running/services/delete/?$', views.api_delete_running_services, name='api_delete_running_services'),

    # Devices
    url(r'^api/devices/?$', views.api_devices, name='api_devices'),
    url(r'^api/devices/delete?$', views.api_delete_devices, name='api_delete_devices'),
    url(r'^api/neds/?$', views.api_neds, name='api_neds'),
    url(r'^api/authgroups/?$', views.api_authgroups, name='api_authgroups'),
    url(r'^api/device_types/?$', views.api_device_types, name='api_device_types'),
    url(r'^api/protocols/?$', views.api_protocols, name='api_protocols'),
    url(r'^api/alerts/?$', views.api_alerts, name='api_alerts'),

    url(r'^api/settings/?$', views.api_settings, name='api_nso'),
]
