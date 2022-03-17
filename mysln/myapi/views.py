from random import gauss
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from .serializers import DHT_dataSerializer, HeroSerializer, Led_dataSerializer, Schedule_dataSerializer
from myapi import models
import os
import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.decorators import action, api_view
from django_filters.rest_framework import DjangoFilterBackend
from mycircuit import led
import string
import random
import mycircuit.mycron as cron


class HeroViewSet(viewsets.ModelViewSet):
    queryset = models.Hero.objects.all().order_by('alias')
    serializer_class = HeroSerializer

    @action(methods=['get'], detail=True)
    def get_by_id(self, request, alias=None):
        if alias:
            # item = Hero.objects.filter(id_gte=id).filter(timestamp_gte = fromtime)
            item = models.Hero.objects.filter(
                alias=alias)
            print(item)
            serializer_class = HeroSerializer


class CarsAPIView(APIView):
    serializer_class = HeroSerializer

    def get_queryset(self):
        cars = models.Hero.objects.all()
        return cars

    def get(self, request, *args, **kwargs):

        try:
            id = request.query_params["id"]
            if id != None:
                car = models.Hero.objects.get(id=id)
                serializer = HeroSerializer(car)

        except:
            cars = self.get_queryset()
            serializer = HeroSerializer(cars, many=True)

        return Response(serializer.data)

class ScheduleManage_Cron(APIView):

    def get(self, request, *args, **kwargs):

        try:
            id = None
            result = ""
            if "id" in request.query_params:
                id = request.query_params["id"]
            if id is None:
                result = cron.listCron()
            
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_200_OK)
    def delete(self, request, *args, **kwargs):
        try:
            id = None
            result = ""
            if "id" in request.query_params:
                cron.removeSpecificCron(request.query_params["id"])
            else :
                cron.removeAllCron()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    def post(self, request, format=None):
        try:
            id = ''.join(random.choices(string.ascii_uppercase +
                                        string.digits, k=10))
            device = request.data["device"]
            devicestatus = request.data["devicestatus"]
            timesettings = request.data["timesettings"]
            if device == "Led":
                if devicestatus == "On":
                    cron.cronAtSpecificTime(
                        "lib-circuit g --turnonled", id, device, devicestatus, timesettings)
                else:
                    cron.cronAtSpecificTime(
                        "lib-circuit g --turnoffled", id, device, devicestatus, timesettings)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class ScheduleManage(APIView):
    serializer_class = Schedule_dataSerializer

    def get_queryset(self):
        print("schedule")
        schedules = models.Schedule.objects.all()
        return schedules

    def get(self, request, *args, **kwargs):

        try:
            id = None
            cronrequest = None
            result = ""
            if "id" in request.query_params:
                id = request.query_params["id"]
            if "cron" in request.query_params:
                cronrequest = request.query_params["cron"]
            if id != None:
                if cronrequest is None or cronrequest == "0":
                    schedule = models.Schedule.objects.get(id=id)
                    serializer = Schedule_dataSerializer(schedule)
                    result = serializer.data
                else:
                    result = cron.listCron()
        except:
            schedules = self.get_queryset()
            serializer = Schedule_dataSerializer(schedules, many=True)

        return Response(result, status=status.HTTP_200_OK)

    

    # def delete(self, request, *args, **kwargs):
    #     try:
    #         id = request.query_params["id"]


class LedManage(APIView):
    serializer_class = Led_dataSerializer

    def get_queryset(self):
        leds = models.Led_Data.objects.all()
        return leds

    def get(self, request, *args, **kwargs):
        try:
            result = ""
            g = led.Led()
            dht = models.DHT_data.objects
            if "ledstatus" in request.query_params:
                led_status = request.query_params["ledstatus"]
                if led_status == "turnon":
                    result = g.turnOn()
                    channel_layer = get_channel_layer()
                    group_name = 'group_led'
                    async_to_sync(channel_layer.group_send)(
                        group_name,
                        {
                            'type': 'led_notification',
                            'target': 'led',
                            'data': {"status": "On"}
                        }
                    )
                elif led_status == "turnoff":
                    result = g.turnOff()
                    channel_layer = get_channel_layer()
                    group_name = 'group_led'
                    async_to_sync(channel_layer.group_send)(
                        group_name,
                        {
                            'type': 'led_notification',
                            'target': 'led',
                            'data': {"status": "Off"}
                        }
                    )
                else:
                    result = g.status()
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)

    def post(self, request, format=None):
        channel_layer = get_channel_layer()
        group_name = 'group_led'
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'led_notification',
                'target': 'led',
                'data': request.data
            }
        )
        return Response(status=status.HTTP_200_OK)


class DHT11Manage(APIView):
    serializer_class = DHT_dataSerializer

    def get_queryset(self):
        dhts = models.DHT_data.objects.all()
        return dhts

    def get(self, request, *args, **kwargs):

        try:
            dht = models.DHT_data.objects
            if "id" in request.query_params:
                id = request.query_params["id"]
                dht = dht.filter(id=id)
            if "fromtime" in request.query_params:
                fromtime = request.query_params["fromtime"]
                dht = dht.filter(timestamp__gte=fromtime)
            if "totime" in request.query_params:
                totime = request.query_params["totime"]
                dht = dht.filter(timestamp__lte=totime)
            serializer = DHT_dataSerializer(dht, many=True)
        except Exception as e:
            print(e)
            dht = self.get_queryset()
            serializer = DHT_dataSerializer(dht, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        channel_layer = get_channel_layer()
        group_name = 'group_dht11'
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'logDHT11_collect',
                'target': 'dht11',
                'data': request.data
            }
        )
        return Response(status=status.HTTP_200_OK)
