from rest_framework import serializers

from lock_owners.models import (Event, Lock, Owner, Permission, StrangerReport,
                                TempAuth)


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ('id', 'username', 'password', 'full_name', 'phone', 'email')


class LockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lock
        fields = ('id', 'lock_owner', 'address')


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
            'visitor',
            'lock',
            'time_created',
            'auth_code'
        )
