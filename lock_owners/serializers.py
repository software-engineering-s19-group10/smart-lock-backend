from rest_framework import serializers
from lock_owners.models import User, Owner, Lock, Permission

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'full_name', 'phone', 'email')
        
class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ('id', 'user')

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