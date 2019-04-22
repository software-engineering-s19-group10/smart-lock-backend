from datetime import datetime
import os
import django.http.response as httpresponse
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from lock_owners.models import Owner, Lock, Permission, Event, StrangerReport, TempAuth
from lock_owners.serializers import OwnerSerializer, StrangerReportSerializer
from lock_owners.serializers import LockSerializer, PermissionSerializer
from lock_owners.serializers import EventSerializer, TempAuthSerializer
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from django.core import serializers
import json
from lock_owners.models import (Event, Lock, Owner, Permission, StrangerReport,
                                TempAuth, Resident, ResidentImage)
from lock_owners.serializers import (EventSerializer, LockSerializer,
                                     OwnerSerializer, PermissionSerializer,
                                     StrangerReportSerializer,
                                     TempAuthSerializer, ResidentSerializer, 
                                     ResidentImageSerializer)

from lock_owners.recognition_utils import bytestring_to_cv, embedFaces

from rest_framework.authtoken.models import Token
import requests
from geopy import geocoders

IMAGES_ADDED = 0

gMapsKey = os.environ['GMAPS_KEY']
# gMapsKey = -1
# client = -1
client = Client(os.environ['TWILIO_SID'], os.environ['TWILIO_AUTH_TOKEN'])
twilio_number = '+18566662253'

class OwnerCreateView(generics.ListCreateAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    #permission_classes = (IsAuthenticated,)
    def perform_create(self, serializer):
        serializer.save()

class OwnerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    #permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            user = Owner.objects.get(id=kwargs.get('pk'))
            serialized = OwnerSerializer(user)
            return Response(serialized.data)
        else:
            raise KeyError('ID cannot be found')

    def patch(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            user = Owner.objects.get(id=kwargs.get('pk'))
            serialized = OwnerSerializer(user, data=request.data, partial=True)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data)
            else:
                return Response(status.HTTP_400_BAD_REQUEST)
        else:
            raise KeyError('ID cannot be found')

    def delete(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            user = Owner.objects.get(id=kwargs.get('pk'))
            user.delete()
            return Response(status.HTTP_200_OK)
        else:
            raise KeyError('ID not found')


class LockCreateView(generics.ListCreateAPIView):
    queryset = Lock.objects.all()
    serializer_class = LockSerializer
    #permission_classes = (IsAuthenticated,)


class LockDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lock.objects.all()
    serializer_class = LockSerializer
    #permission_classes = (IsAuthenticated,)


class PermissionCreateView(generics.ListCreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    #permission_classes = (IsAuthenticated,)


class PermissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    #permission_classes = (IsAuthenticated,)


class EventCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    #permission_classes = (IsAuthenticated,)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    #permission_classes = (IsAuthenticated,)

#class VisitorImageView(generics.ListCreateAPIView):
#    queryset = VisitorImage.objects.all()
#    serializer_class = VisitorImageSerializer



class StrangerReportView(generics.ListCreateAPIView):
    queryset = StrangerReport.objects.all()
    serializer_class = StrangerReportSerializer

#class VisitorImageView(generics.ListCreateAPIView):
#    queryset = VisitorImage.objects.all()
#    serializer_class = VisitorImageSerializer


class ResidentCreateView(generics.ListCreateAPIView):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer


class ResidentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer


class ResidentImageCreateView(generics.ListCreateAPIView):
    queryset = ResidentImage.objects.all()
    serializer_class = ResidentImageSerializer

    def perform_create(self, serializer):
        with open('lock_owners/image_added.txt', 'w+') as images_added:
            images_added.seek(0)
            images_added.write('1')
            images_added.truncate()
        serializer.save()


class ResidentImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ResidentImage.objects.all()
    serializer_class = ResidentImageSerializer


def get_residents_for_lock(request):
    if request.method == 'GET':
        try:
            residents = Resident.objects.filter(lock=request.GET['lock'])
            if not residents:
                data = {
                    'status': 200,
                    'message': 'No residents for lock',
                    'data': []
                }
                return JsonResponse(data)
            residents_json = []
            for resident in list(residents):
                residents_json.append({
                    'id': resident.id,
                    'full_name': resident.full_name,
                    'lock': resident.lock.id
                })
                data = {
                    'status': 200,
                    'message': 'Success',
                    'data': residents_json
                }
                return JsonResponse(data)
        except KeyError:
            data = {
                'status': 404,
                'message': 'No lock ID was specified'
            }
            return JsonResponse(data)


def get_residents_for_owner(request):
    if request.method == 'GET':
        try:
            locks = Lock.objects.filter(lock_owner=request.GET['owner'])
            if not locks:
                data = {
                    'status': 200,
                    'message': 'No locks associated with the Owner',
                    'data': []
                }
                return JsonResponse(data)
            owner_locks = list(locks.values('id'))
            lock_ids = [item.get('id') for item in owner_locks]
            residents = Resident.objects.filter(lock__in=lock_ids)
            if not residents:
                data = {
                    'status': 200,
                    'message': 'No residents associated with the Owner locks',
                    'data': []
                }
                return JsonResponse(data)
            residents_json = []
            for resident in list(residents):
                residents_json.append({
                    'id': resident.id,
                    'full_name': resident.full_name,
                    'lock': resident.lock.id
                })
                data = {
                    'status': 200,
                    'message': 'Success',
                    'data': residents_json
                }
                return JsonResponse(data)
        except KeyError:
            data = {
                'status': 404,
                'message': 'No Owner ID was passed into the URL'
            }

def get_events_for_lock(request, id):
    if request.method == 'GET':
        events = Event.objects.filter(lock=id)
        events_json = []
        for event in events:
            event_json = {}
            event_json['id'] = event.id
            event_json['event_type'] = event.event_type
            event_json['lock'] = event.lock.id
            event_json['timestamp'] = str(event.timestamp)
            event_json['duration'] = event.duration
            events_json.append(event_json)
        data = {
            'status': 200,
            'message': 'Success',
            'data': events_json
        }
        return JsonResponse(data)

def get_events_for_user(request):
    if request.method == 'GET':
        try:
            owner_locks = Lock.objects.filter(lock_owner=request.GET['owner'])
            if not owner_locks:
                data = {
                    'status': 404,
                    'message': 'No locks exist for the owner'
                }
                return JsonResponse(data)
                
            owner_locks = list(owner_locks.values('id'))
            lock_ids = [item.get('id') for item in owner_locks]
            events = Event.objects.filter(lock__in=lock_ids)
            if not events:
                data = {
                    'status': 404,
                    'message': 'No events exist for the owner'
                }
                return JsonResponse(data)

            events_json = []
            for event in list(events):
                events_json.append({
                    'id': event.id,
                    'event_type': event.event_type,
                    'lock': event.lock.id,
                    'timestamp': str(event.timestamp),
                    'duration': event.duration
                })
            data = {
                'status': 200,
                'message': 'Success',
                'data': events_json
            }
            return JsonResponse(data)
        except KeyError:
            data = {
                'status': 404,
                'message': 'No owner ID was specified in the request'
            }
            return JsonResponse(data)



class TempAuthCreateView(generics.ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    queryset = TempAuth.objects.all()
    serializer_class = TempAuthSerializer

    def perform_create(self, serializer):
        serializer.is_valid()
        print(serializer.validated_data)
        existing_auths = TempAuth.objects.filter(visitor=serializer.validated_data['visitor'], lock=serializer.validated_data['lock'])
        if existing_auths.exists():
            raise ValidationError('Only one auth code per user allowed')
        serializer.save()

class TempAuthDetailView(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = (IsAuthenticated,)
    queryset = TempAuth.objects.all()
    serializer_class = TempAuthSerializer


def verify_auth_code(request):
    if request.method == 'GET':
        try:
            auth_code = request.GET['auth_code']
            print(auth_code)
            temp_auth = TempAuth.objects.filter(auth_code=auth_code)
            if not temp_auth:
                data = {
                    'message': 'Temporary auth code does not exist',
                    'status': 404
                }
                return JsonResponse(data)
            current_datetime = timezone.now()
            if (current_datetime - temp_auth[0].time_created).days >= 1:
                data = {
                    'message': 'Auth code timed out (more than a day old)', 
                    'status': 404
                }
                temp_auth[0].delete()
                return JsonResponse(data)
            else:
                data = {
                    'message': 'Success', 
                    'status': 200
                }
                temp_auth[0].delete()
                return JsonResponse(data)
        except KeyError as e:
            data = {'message': str(e), 'status': 404}
            return JsonResponse(data)
            

def get_temp_auth_id_for_visitor_and_lock(request):
    if request.method == 'GET':
        try:
            visitor = request.GET['visitor']
            lock = request.GET['lock']
            temp_auth = TempAuth.objects.filter(visitor=visitor, lock=lock)
            if not temp_auth:
                data = {
                    'message': 'Could not find temp auth for visitor/lock pair',
                    'status': 404
                }
                return JsonResponse(data)
            auth_id = temp_auth[0].id
            data = {
                'id': auth_id,
                'status': 200
            }
            return JsonResponse(data)
        except KeyError:
            data = {
                'message': 'Missing visitor ID or lock ID in request',
                'status': 404
            }
            return JsonResponse(data)


def get_auth_code_for_id(request):
    if request.method == 'GET':
        try:
            auth_id = request.GET['id']
            temp_auth = TempAuth.objects.filter(id=auth_id)
            if not temp_auth:
                data = {
                    'message': 'No auth code exists for ID',
                    'status': 404
                }
                return JsonResponse(data)
            auth_code = temp_auth[0].auth_code
            data = {
                'auth_code': auth_code,
                'status': 200
            }
            return JsonResponse(data)
        except KeyError:
            data = {
                'message': 'Temp Auth ID must be specified in request',
                'status': 404
            }
            return JsonResponse(data)

def get_user_id_for_token(request):
    if request.method == 'GET':
        try:
            token = Token.objects.filter(key=request.GET['token'])
            if not token:
                data = {
                    'status': 404,
                    'message': 'Could not get user ID for the token'
                }
                return JsonResponse(data)
            user_id = token[0].user_id
            data = {
                'status': 200,
                'message': 'Successfully got the user ID',
                'id': user_id
            }
            return JsonResponse(data)
        except KeyError:
            data = {
                'status': 404,
                'message': 'Must send a token to get the user ID for'
            }
            return JsonResponse(data)


def get_temp_auths_for_lock(request):
    if request.method == 'GET':
        try:
            temp_auths = TempAuth.objects.filter(lock=request.GET['lock'])
            if not temp_auths:
                data = {
                    'status': 404,
                    'message': 'No temp auths for lock ID'
                }
                return JsonResponse(data)
            temp_auths_list = list(temp_auths)
            temp_auths_json = []
            for auth in list(temp_auths):
                temp_auths_json.append({
                    'id': auth.id,
                    'visitor': auth.visitor,
                    'lock': auth.lock.id,
                    'time_created': str(auth.time_created),
                    'auth_code': str(auth.auth_code)
                })       
            print(temp_auths_json)  
            data = {
                'status': 200,
                'message': 'Success',
                'data': temp_auths_json
            }
            return JsonResponse(data)
        except KeyError:
            data = {
                'status': 404,
                'message': 'No lock ID specified'
            }

def get_locks_for_owner(request):
    if request.method == 'GET':
        try:
            locks = Lock.objects.filter(lock_owner=request.GET['owner'])
            if not locks:
                data = {
                    'status': 200,
                    'message': 'Success',
                    'data': []
                }
                return JsonResponse(data)
            locks_json = []
            for item in list(locks):
                locks_json.append({
                    'id': item.id,
                    'lock_owner': item.lock_owner.id,
                    'address': item.address
                })
            data = {
                'status': 200,
                'message': 'Success',
                'data': locks_json
            }
            return JsonResponse(data)
        except KeyError:
            data = {
                'status': 404,
                'message': 'No user ID was passed in with the request.'
            }
            return JsonResponse(data)


def get_embedded_data(request):
    if request.method == 'GET':
        with open('lock_owners/image_added.txt', 'r+') as images_added:
            print(images_added)
            images_added.seek(0)
            new_images = images_added.read()
            print(new_images)
            if new_images == '1':
                resident_images = ResidentImage.objects.all()
                resident_image_list = []
                for image in list(resident_images):
                    resident = list(Resident.objects.filter(id=image.resident.id))
                    resident_name = resident[0].full_name
                    resident_image_list.append({
                        'name': resident_name,
                        'image_bytes': image.image_bytes
                    })
                #print(resident_image_list)
                data = embedFaces(resident_image_list)
                #print(data)
                images_added.seek(0)
                images_added.write('0')
                images_added.truncate()
                return JsonResponse(data, safe=False)
            else:
                data = {
                    'status': 404,
                    'message': 'No new images added'
                }
                return JsonResponse(data)

#def create_img_template(request):
#    if request.method == "GET":
#
#        lock = request.GET["lock"]
#        filename = request.GET["filename"]
#
#        strangerImage = VisitorImage.objects.filter(lock=lock, #filename=filename)
#        img_buffer = strangerImage[0].image
#
#        html = "<html><body><img src=\"data:image/jpg;base64,#%s\"></img></body></html>" % base64.b64encode(img_buffer).decode#('utf-8')
#        return HttpResponse(html)


def send_text(request):
    if request.method == "POST":
        if request.POST["type"] == "srn":
            lock = request.POST["lock"]
            filename = request.POST["file"]
            url = "https://boiling-reef-89836.herokuapp.com/lock_owners/api/image/?" + "lock=" + lock + "&filename=" + filename
            response = request.POST["content"] + " IMAGE: " + url + "  Reply REPORT to report."
        else:
            response = request.POST["content"] + " Reply STOP to stop SMS notifications."

        message = client.messages.create(
            from_=twilio_number,
            body=response,
            to="+" + request.POST["dest"]
        )

        data = {
            'message': "Success.",
            'status': 200
        }
        return JsonResponse(data)

def reply(request):
    """Respond to incoming messages with a friendly SMS."""
    if request.method == "POST":
        # Get information about the
        number = request.form['From']
        message_body = request.form['Body']

        if message_body == "STOP":
            # do action to stop sms notifications for user
            text = "You have unsubscribed from SMS notifications."
        elif message_body == "REPORT":
            # Report the stranger report
            owner = Owner.objects.filter(phone=number)
            if not owner:
                return "User not found"
            else:
                # get lock
                lock = Lock.objects.filter(lock_owner=owner)
                address = lock[0].address

                geolocator = geocoders.GoogleV3(api_key=gMapsKey)

                location = geolocator.geocode(address, timeout=10)

                BASE_URL = "https://boiling-reef-89836.herokuapp.com/lock_owners/"
                route = 'api/srn/'
                params = {"latitude": location.latitude, "longitude": location.longitude,
                          "stranger_report_time": datetime.now(), "lock": lock[0].id}

                requests.post(BASE_URL + route, params)
                return

        else:
            text = "Invalid Response. Reply STOP to stop SMS notifications."

        # Start our response
        resp = MessagingResponse()

        # Add a message
        resp.message(text)

        return str(resp)
