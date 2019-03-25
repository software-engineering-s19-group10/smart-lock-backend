from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from lock_owners.models import User, Lock, Permission, Event, StrangerReport
from lock_owners.serializers import UserSerializer, StrangerReportSerializer
from lock_owners.serializers import LockSerializer, PermissionSerializer
from lock_owners.serializers import EventSerializer
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from rest_framework.views import APIView
import django.http.response as httpresponse
from django.http import HttpResponse, JsonResponse
from django.core import serializers

from lock_owners.models import Lock, Permission, User
from lock_owners.serializers import (LockSerializer, PermissionSerializer,
                                     UserSerializer)

class UserCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    def perform_create(self, serializer):
        serializer.save()

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            user = User.objects.get(id=kwargs.get('pk'))
            serialized = UserSerializer(user)
            return Response(serialized.data)
        else:
            raise KeyError('ID cannot be found')

    def patch(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            user = User.objects.get(id=kwargs.get('pk'))
            serialized = UserSerializer(user, data=request.data, partial=True)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data)
            else:
                return Response(status.HTTP_400_BAD_REQUEST)
        else:
            raise KeyError('ID cannot be found')

    def delete(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            user = User.objects.get(id=kwargs.get('pk'))
            user.delete()
            return Response(status.HTTP_200_OK)
        else:
            raise KeyError('ID not found')


class LockCreateView(generics.ListCreateAPIView):
    queryset = Lock.objects.all()
    serializer_class = LockSerializer
    permission_classes = (IsAuthenticated,)


class LockDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lock.objects.all()
    serializer_class = LockSerializer
    permission_classes = (IsAuthenticated,)


class PermissionCreateView(generics.ListCreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = (IsAuthenticated,)


class PermissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = (IsAuthenticated,)


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


# Your Account Sid and Auth Token from twilio.com/console
key_reader = open("lock_owners/key.txt", "r")
account_sid = key_reader.readline()
auth_token = key_reader.readline()
client = Client(account_sid, auth_token)
twilio_number = '+18566662253'

def send_text(request):
    response = request.GET["content"] + " Reply STOP to stop SMS notifications."

    message = client.messages.create(
        from_=twilio_number,
        body=response,
        to="+" + request.GET["dest"]
    )

    return httpresponse.HttpResponse("Successful")


# DISCLAIMER: MMS and REPLY don't work yet
def send_mms(request):
    # get uid from mms
    response = request.POST.get("content") + " Reply STOP to stop SMS notifications."
    message = client.messages.create(
        body=response,
        from_=twilio_number,
        media_url=request.POST.get("img_url"),
        to=request.POST.get("dest")
    )

    # if request.get("method") == "POST":
    # send dj http response. send dictionary back
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
