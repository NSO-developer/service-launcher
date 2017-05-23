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
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

"""******** Network Element Drivers ********"""


class NED(models.Model):
    """
    Database model for NEDs
    """
    name = models.CharField(max_length=200)
    xmlns = models.CharField(max_length=200)
    ned_id = models.CharField(max_length=200)
    prefix = models.CharField(max_length=200)


"""******** Device type options  ********"""


class DeviceType(models.Model):
    """
    Database for device types
    """
    name = models.CharField(max_length=200)


"""******** Connection protocol options  ********"""


class Protocol(models.Model):
    """
    Database for protocol options
    """
    name = models.CharField(max_length=200)
