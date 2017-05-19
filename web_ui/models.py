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
