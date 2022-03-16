
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from .serializers import DHT_dataSerializer, HeroSerializer
from myapi import models
import os
import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend


class HeroViewSet(viewsets.ModelViewSet):
    print("con cac")
    queryset = models.Hero.objects.all().order_by('alias')
    serializer_class = HeroSerializer
    print("con cac")

    @action(methods=['get'], detail=True)
    def get_by_id(self, request, alias=None):
        print("ddd")
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
            print(dht)
            serializer = DHT_dataSerializer(dht, many=True)
        except Exception as e:
            print(e)
            dht = self.get_queryset()
            serializer = DHT_dataSerializer(dht, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        channel_layer = get_channel_layer()
        group_name = 'group_DHT11'
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'logDHT11_collect',
                'data': request.data
            }
        )
        return Response(status=status.HTTP_200_OK)
