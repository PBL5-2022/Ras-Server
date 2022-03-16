# serializers.py
from rest_framework import serializers

from myapi import models


class HeroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Hero
        fields = ('name', 'alias')


class DHT_dataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DHT_data
        fields = ('id', 'timestamp', 'temp', 'hum')


class Led_dataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Led_Data
        fields = ('id', 'timestamp', 'status')
