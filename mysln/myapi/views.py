from http.client import BAD_REQUEST
from random import gauss
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from .serializers import BH1750_dataSerializer, DHT_dataSerializer, HeroSerializer, Led_dataSerializer, Schedule_dataSerializer, UserLoginSerializer, UserSerializer
from myapi import models
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.decorators import action, api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from mycircuit import led
import string
import random
import mycircuit.mycron as cron
from django.contrib.auth import authenticate, login, logout, hashers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import AllowAny


class UserRegisterView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password'] = hashers.make_password(
                serializer.validated_data['password'])
            user = serializer.save()

            return Response('Register oke', status=status.HTTP_201_CREATED)

        else:
            return Response("Email has already exist", status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = TokenObtainPairSerializer.get_token(user)
                data = {
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token),
                    'access_expires': int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
                    'refresh_expires': int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds())
                }
                return Response(data, status=status.HTTP_200_OK)

            return Response({
                'error_message': 'Email or password is incorrect!',
                'error_code': 400
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'error_messages': serializer.errors,
            'error_code': 400
        }, status=status.HTTP_400_BAD_REQUEST)


class HeroViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
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
            else:
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
            if "Led" in device:
                lednum = int(device.replace("Led", ""))
                if devicestatus == "On":
                    cron.cronAtSpecificTime(
                        f"lib-circuit {lednum} --onled", id, device, devicestatus, timesettings)
                else:
                    cron.cronAtSpecificTime(
                        f"lib-circuit {lednum} --offled", id, device, devicestatus, timesettings)
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
            if "ledname" in request.query_params:
                lednum = int(
                    request.query_params["ledname"].replace("Led", ""))
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            result = ""
            g = led.Led()
            dht = models.DHT_data.objects
            if "ledstatus" in request.query_params:
                led_status = request.query_params["ledstatus"]
                if led_status == "turnon":
                    result = g.turnOn(lednum)
                    channel_layer = get_channel_layer()
                    group_name = 'group_led'
                    async_to_sync(channel_layer.group_send)(
                        group_name,
                        {
                            'type': 'led_notification',
                            'target': 'led',
                            'data': {
                                "status": "On",
                                "ledname": request.query_params["ledname"]
                            }
                        }
                    )
                elif led_status == "turnoff":
                    result = g.turnOff(lednum)
                    channel_layer = get_channel_layer()
                    group_name = 'group_led'
                    async_to_sync(channel_layer.group_send)(
                        group_name,
                        {
                            'type': 'led_notification',
                            'target': 'led',
                            'data': {
                                "status": "Off",
                                "ledname": request.query_params["ledname"]
                            }
                        }
                    )
                elif led_status == "status":
                    result = g.status(lednum)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

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


class BH1750Manage(APIView):
    serializer_class = BH1750_dataSerializer

    def get_queryset(self):
        bh1750s = models.BH1750_data.objects.all()
        return bh1750s

    def get(self, request, *args, **kwargs):

        try:
            bh1750 = models.BH1750_data.objects
            if "id" in request.query_params:
                id = request.query_params["id"]
                bh1750 = bh1750.filter(id=id)
            if "fromtime" in request.query_params:
                fromtime = request.query_params["fromtime"]
                bh1750 = bh1750.filter(timestamp__gte=fromtime)
            if "totime" in request.query_params:
                totime = request.query_params["totime"]
                bh1750 = bh1750.filter(timestamp__lte=totime)
            serializer = BH1750_dataSerializer(bh1750, many=True)
        except Exception as e:
            print(e)
            bh1750 = self.get_queryset()
            serializer = BH1750_dataSerializer(bh1750, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        channel_layer = get_channel_layer()
        group_name = 'group_bh1750'
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'bh1750_collect',
                'target': 'bh1750',
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
