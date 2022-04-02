# serializers.py
from rest_framework import serializers

from myapi import models


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class HeroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Hero
        fields = ('name', 'alias')


class DHT_dataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DHT_data
        fields = ('id', 'timestamp', 'temp', 'hum')


class Device_dataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Device
        fields = ('name', 'type', 'location', 'status')


class BH1750_dataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BH1750_data
        fields = ('id', 'timestamp', 'lightlevel')


class Led_dataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Led_Data
        fields = ('id', 'timestamp', 'status', 'ledname')


class Schedule_dataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Schedule
        fields = ('id', 'timestamp', 'device', 'status', 'timesetting')
