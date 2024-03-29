# models.py
from django.db import models
from django.conf import settings
import time

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Delete not use field
    username = None
    last_login = None
    is_staff = None
    is_superuser = None

    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Hero(models.Model):
    name = models.CharField(max_length=60)
    alias = models.CharField(max_length=60)

    def __str__(self):
        return self.name


# class UserStatus(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userstatus')
#     status = models.BooleanField(default=False)

#     def __str__(self):
#         return f"UserStatus of {self.user.username}"


class Device(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    type = models.CharField(max_length=60)
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=60)

class DHT_data(models.Model):

    # id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(null=False)
    temp = models.DecimalField(max_digits=15, decimal_places=6)
    hum = models.DecimalField(max_digits=15, decimal_places=6)
    # order items in descending order

    class Meta:
        ordering = ["-timestamp"]

    # the method which defines string output of class
    def __str__(self):
        return str(self.timestamp)


class BH1750_data(models.Model):

    # id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(null=False)
    lightlevel = models.DecimalField(max_digits=15, decimal_places=6)
    # order items in descending order

    class Meta:
        ordering = ["-timestamp"]

    # the method which defines string output of class
    def __str__(self):
        return str(self.timestamp)


class Led_Data(models.Model):
    timestamp = models.DateTimeField(null=False, default='2022-01-01')
    # 1 la den sang , 0 la den tat
    status = models.BooleanField(null=False, default=False)
    ledname = models.CharField(max_length=20)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return str(self.status + " : "+self.timestamp+" : "+self.ledname)

class Door_Data(models.Model):
    timestamp = models.DateTimeField(null=False, default='2022-01-01')
    status = models.BooleanField(null=False, default=False)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return str(self.status + " : "+self.timestamp)


class Motor_Data(models.Model):
    timestamp = models.DateTimeField(null=False, default='2022-01-01')
    # 1 la den sang , 0 la den tat
    dutycycle = models.IntegerField()
    motorname = models.CharField(max_length=20)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return str(self.duty_cycle + " : "+self.timestamp+" : "+self.motorname)
    
    

class Schedule(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    device = models.CharField(max_length=60)
    status = models.CharField(max_length=60)
    timesetting = models.CharField(max_length=60)
    timestamp = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.id+" :"+self.device + " : "+self.timesetting+" : "+self.status+": "+self.timestamp)


class GroupChannel(models.Model):
    channelname = models.CharField(max_length=500)
    groupname = models.CharField(max_length=100)

 