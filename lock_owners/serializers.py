from rest_framework import serializers

from lock_owners.models import (Event, Lock, Owner, Permission, StrangerReport,
                                TempAuth, Resident, ResidentImage, VisitorImage)


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ('id', 'username', 'password', 'full_name', 'phone', 'email')


class LockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lock
        fields = ('id', 'lock_owner', 'address', 'ip_address')


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = (
            'id', 
            'user', 
            'lock', 
            'allowed_access_general', 
            'time_start', 
            'time_end'
        )

class VisitorImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitorImage
        fields = (
            'image',
            'filename',
            'name',
            'lock',
            'image_datetime',
        )


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'timestamp',
            'duration',
            'lock',
            'event_type'
        )


class StrangerReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrangerReport
        fields = (
            'latitude',
            'longitude',
            'stranger_report_time',
            'lock'
        )

class TempAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempAuth
        fields = (
            'id',
            'visitor',
            'lock',
            'time_created',
            'auth_code'
        )

class ResidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        fields = (
            'id',
            'full_name',
            'lock'
        )

class ResidentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidentImage
        fields = (
            'id',
            'resident',
            'image_bytes'
        )