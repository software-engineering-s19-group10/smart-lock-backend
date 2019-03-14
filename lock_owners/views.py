from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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
