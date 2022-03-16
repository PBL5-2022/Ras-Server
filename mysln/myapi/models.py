# models.py
from django.db import models
from django.conf import settings


class Hero(models.Model):
    name = models.CharField(max_length=60)
    alias = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class UserStatus(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userstatus')
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"UserStatus of {self.user.username}"


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


class Led_Data(models.Model):
    timestamp = models.DateTimeField(null=False)
    status = models.BooleanField(null=False)  # 1 la den sang , 0 la den tat
    
    class Meta:
        ordering = ["-timestamp"]
        
    def __str__(self):
        return str(self.status + " : "+self.timestamp)
