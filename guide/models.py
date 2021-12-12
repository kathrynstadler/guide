# REFERENCES
# Title: Django-CRUM
# Author: Python Hosted
# Date: 11/29/2021
# Code version: 0.7.2
# URL: https://pythonhosted.org/django-crum/
# Software License: BSD

import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.models import User
from crum import get_current_user
from phonenumber_field.modelfields import PhoneNumberField


class PointOfInterest(models.Model):
    name = models.CharField(max_length=128)
    latitude = models.DecimalField(
        max_digits=10, 
        decimal_places=8
    )
    longitude = models.DecimalField(
        max_digits=11,
        decimal_places=8
    )
    review = models.CharField(max_length=4096)

    def __str__(self):
        return self.name


class Reviews(models.Model):
    location = models.CharField(max_length=200)
    review = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.location


class Request(models.Model):
    name = models.CharField(max_length=200, default = None)
    address = models.CharField(max_length=200, default = None)
    created_date = models.DateTimeField(default=timezone.now)
    latitude = models.CharField(max_length=200, default = '0') 
    longitude = models.CharField(max_length=200, default = '0')

    def __str__(self):
        return self.name


class UserInformation(models.Model):
    created_by = models.ForeignKey('auth.User', blank=True, null=True, default=None, on_delete=models.PROTECT)
    address = models.CharField(max_length=200, default='NONE')
    city = models.CharField(max_length=50, default='Charlottesville')
    state = models.CharField(max_length=2, default='VA')
    zipcode = models.CharField(max_length=5, default='22903')
    phone_number = PhoneNumberField(default='NONE', region='US')

    def save(self, *args, **kwargs):
        # Django-CRUM get_current_user()
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        super(UserInformation, self).save(*args, **kwargs)

    def __str__(self):
        return self.address
