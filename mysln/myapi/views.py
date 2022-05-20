from http.client import BAD_REQUEST
from random import gauss
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BH1750_dataSerializer, DHT_dataSerializer, Device_dataSerializer, HeroSerializer, Led_dataSerializer, Motor_dataSerializer, UploadSerializer, Schedule_dataSerializer, UserLoginSerializer, UserSerializer
from myapi import models
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.decorators import action, api_view, permission_classes
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
from django.core.files.storage import FileSystemStorage
import requests
import json

door_data_path = "/home/pi/Ras-Server/mysln/mycircuit/data_rfid.txt"
fan_data_path = "/home/pi/Ras-Server/mysln/mycircuit/data_rfid.txt"
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

class ScheduleManage(APIView):
    permission_classes = (AllowAny,)
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



class ScheduleManage_Cron(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):

        try:
            id = None
            result = []
            if "id" in request.query_params:
                id = request.query_params["id"]
                print(id)
                cron_model = models.Schedule.objects.filter(id=id)
            if id is None:
                result = cron.listCron()
                cron_model = models.Schedule.objects.filter(id__in=result)
            serializer = Schedule_dataSerializer(cron_model, many=True)
            return Response(serializer.data)

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
            if "led" in device:
                lednum = int(device.replace("led", ""))
                if devicestatus == "on":
                    cron.cronAtSpecificTime(
                        f"lib-circuit {lednum} --onled", id, device, devicestatus, timesettings)
                else:
                    cron.cronAtSpecificTime(
                        f"lib-circuit {lednum} --offled", id, device, devicestatus, timesettings)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UploadViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UploadSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        file_uploaded = request.FILES['file_uploaded']

        # response = requests.post(
        #     'http://localhost:8000/test/', files={'file_uploaded': file_uploaded})

        if file_uploaded:
            # save attached file

            # create a new instance of FileSystemStorage
            fs = FileSystemStorage()
            file = fs.save(file_uploaded.name, file_uploaded)
            # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
            fileurl = fs.url(file)
        response = f"POST API and you have uploaded a {fileurl} file"
        return Response(response)


class TestReceiveFile(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        file_uploaded = request.FILES['file_uploaded']

        if file_uploaded:
            # save attached file

            # create a new instance of FileSystemStorage
            fs = FileSystemStorage()
            file = fs.save(file_uploaded.name, file_uploaded)
            # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
            fileurl = fs.url(file)

        response = f"POST API and you have uploaded a {fileurl} file"
        return Response(response)




class LedManage(APIView):
    permission_classes = (AllowAny,)
    serializer_class = Led_dataSerializer

    def get_queryset(self):
        leds = models.Led_Data.objects.all()
        return leds

    def post(self, request, format=None):
        try:
            if "name" in request.data:
                lednum = int(
                    request.data["name"].replace("led", ""))
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            result = ""
            g = led.Led()
            dht = models.DHT_data.objects
            if "status" in request.data:
                led_status = request.data["status"]
                if led_status == "on":
                    result = g.turnOn(lednum)
                    requests.post(
                    'http://localhost:8000/notification', json={
                        "group_name" :'group_led',
                        "target" : 'led',
                        "type" : 'led_notification',
                        "value" :json.dumps({"action": "on" , "name" : request.data["name"]})
                    })
                elif led_status == "off":
                    result = g.turnOff(lednum)
                    requests.post(
                    'http://localhost:8000/notification', json={
                        "group_name" :'group_led',
                        "target" : 'led',
                        "type" : 'led_notification',
                        "value" :json.dumps({"action": "off" , "name" : request.data["name"]})
                    })
                elif led_status == "status":
                    result = g.status(lednum)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)



class Notification(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        channel_layer = get_channel_layer()
        group_name = request.data['group_name']
        print(type(request.data))
        print(str(request.data['value']))
        print(request.data['type'])
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': request.data['type'],
                'target': request.data['target'],
                'data': json.loads(request.data['value'])
            }
        )
        return Response(status=status.HTTP_200_OK)

class MotorManage(APIView):
    permission_classes = (AllowAny,)
    serializer_class = Motor_dataSerializer

    def get_queryset(self):
        motors = models.Motor_Data.objects.all()
        return motors

    def get(self, request, *args, **kwargs):
        try:
            dht = models.Device.objects
            if "name" in request.query_params:
                dht = dht.filter(name=request.query_params["name"])
            if "type" in request.query_params:
                dht = dht.filter(type=request.query_params["type"])
            if "location" in request.query_params:
                dht = dht.filter(location=request.query_params["location"])
            if "status" in request.query_params:
                dht = dht.filter(status=request.query_params["status"])
            serializer = Device_dataSerializer(dht, many=True)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

    def post(self, request, format=None):
        try:
            name = request.data["name"]
            value = request.data["value"]

            with open('/home/pi/Ras-Server/mysln/mycircuit/data_motor.txt', 'r') as file:
                data = file.readlines()
            if name == 'fan1':
                data[0] = f'motor1,{value}\n'
            elif name == 'fan2':
                data[1] = f'motor2,{value}\n'
            with open('/home/pi/Ras-Server/mysln/mycircuit/data_motor.txt', 'w') as file:
                file.writelines(data)

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)



class DoorManage(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        try:
            action = request.data["action"]
            with open(door_data_path, 'r') as file:
                data = file.readlines()
            if action == 'on':
                data[2] = f'checkDoor:True\n'
                data[1] = f'countFalse:0\n'
            elif action == 'off':
                data[2] = f'checkDoor:False\n'
                data[1] = f'countFalse:{int(data[1].split(":")[1])+1}\n'
            elif action =="stop-warning":
                data[2] = f'checkDoor:False\n'
                data[1] = f'countFalse:0\n'
            else :
                return Response(status=status.HTTP_400_BAD_REQUEST)
            data[0] = f'trigger:True\n'
            with open(door_data_path, 'w') as file:
                file.writelines(data)
            file.close()

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)




class BH1750Manage(APIView):
    permission_classes = (AllowAny,)
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



class DeviceManage(APIView):
    permission_classes = (AllowAny,)
    serializer_class = Device_dataSerializer

    def get_queryset(self):
        devices = models.Device.objects.all()
        return devices

    def get(self, request, *args, **kwargs):
        try:
            dht = models.Device.objects
            if "name" in request.query_params:
                dht = dht.filter(name=request.query_params["name"])
            if "type" in request.query_params:
                dht = dht.filter(type=request.query_params["type"])
            if "location" in request.query_params:
                dht = dht.filter(location=request.query_params["location"])
            if "status" in request.query_params:
                dht = dht.filter(status=request.query_params["status"])
            serializer = Device_dataSerializer(dht, many=True)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        try:
            device = models.Device.objects
            if "name" in request.query_params:
                device = device.filter(name=request.query_params["name"])
                device.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer = Device_dataSerializer(data=request.data)
            if serializer.is_valid():
                device = serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            error_list = [serializer.errors[error][0]
                          for error in serializer.errors]
            return Response(error_list, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class DHT11Manage(APIView):
    permission_classes = (AllowAny,)
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
