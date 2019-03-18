from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from lock_owners.models import User, Lock, Permission
from lock_owners.serializers import UserSerializer, StrangerReportSerializer
from lock_owners.serializers import LockSerializer, PermissionSerializer
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from rest_framework.views import APIView

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


class StrangerReportView(generics.ListCreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = StrangerReportSerializer


# Your Account Sid and Auth Token from twilio.com/console
account_sid = 'AC1a776f3f8a6c40eca9c8a7b1669fa713'
auth_token = 'cf97390a0f0cdb9c6c2ec296d1858d41'
client = Client(account_sid, auth_token)
twilio_number = '+18566662253'


def send_text(request):
    reponse = request.get("content") + " Reply STOP to stop SMS notifications."
    message = client.messages.create(
        from_=twilio_number,
        body=reponse,
        to=request.get("dest")
    )

    print(message.sid)


def send_mms(request):
    # get uid from mms
    uid = request.get("uid")

    response = request.get("content") + " Reply STOP to stop SMS notifications."
    message = client.messages.create(
        body=response,
        from_=twilio_number,
        media_url=request.get("img_url"),
        to=request.get("dest")
    )

    request.get("method") == "POST"
    # send dj http response. send dictionary back
    print(message.sid)


def sms(request):
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