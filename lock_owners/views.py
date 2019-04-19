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
from rest_framework.views import APIView
import django.http.response as httpresponse
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from datetime import datetime
from django.utils import timezone
import os
from lock_owners.models import Lock, Permission, Owner
from lock_owners.serializers import (LockSerializer, PermissionSerializer,
                                     OwnerSerializer)

# Library to access heroku environment variables
from boto.s3.connection import S3Connection


# Get the sid and auth token. change depending on environment variable names
#client = Client(os.environ['TWILIO_SID'], os.environ['TWILIO_AUTH_TOKEN'])
#twilio_number = '+18566662253'


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


class StrangerReportView(generics.ListCreateAPIView):
    queryset = StrangerReport.objects.all()
    serializer_class = StrangerReportSerializer


def get_events_for_lock(request, id):
    if request.method == 'GET':
        events = Event.objects.filter(lock=id)
        events_json = []
        for event in events:
            event_json = {}
            event_json['timestamp'] = str(event.timestamp)
            event_json['duration'] = event.duration
            event_json['lock'] = event.lock.id
            event_json['event_type'] = event.event_type
            events_json.append(event_json)
        return HttpResponse(str(events_json), content_type='json')


class TempAuthCreateView(generics.ListCreateAPIView):
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


def send_text(request):
    
    response = request.GET["content"] + " Reply STOP to stop SMS notifications."

    message = client.messages.create(
        from_=twilio_number,
        body=response,
        to="+" + request.GET["dest"]
    )

    return httpresponse.HttpResponse("Successful")

def reply(request):
    """Respond to incoming messages with a friendly SMS."""
    # Get information about the
    number = request.form['From']
    message_body = request.form['Body']

    if message_body == "STOP":
        # do action to stop sms notifications for user
        text = "You have unsubscribed from SMS notifications."
    else:
        text = "Invalid Response. Reply STOP to stop SMS notifications."

    # Start our response
    resp = MessagingResponse()

    # Add a message
    resp.message(text)

    return str(resp)
