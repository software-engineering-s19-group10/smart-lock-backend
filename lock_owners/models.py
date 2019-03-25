import binascii
import os

from django.db import models
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from smartlock_backend import settings
from datetime import datetime

# Create your models here.
class User(AbstractUser):
    """
    Database model for a user of our system. A user is just someone who uses 
    the system.
    """

    full_name = models.CharField(
        help_text='Full name of the user',
        max_length=200,
        null=False,
        blank=False
    )
    
    phone = models.CharField(
        help_text='User phone number (no spaces or dashes, 10 character max)',
        max_length=10
    )

    def __str__(self):
        return '{} ({})'.format(str(self.full_name), str(self.username))  


class Visitor(models.Model):
    """
    Database model representing a general visitor for a lock.
    Visitors can be granted access for locks.
    """

    full_name = models.CharField(
        help_text='Name of the visitor',
        max_length=200,
        null=False,
        blank=False
    )


class Lock(models.Model):
    """
    Database model for a smart lock. Contains useful info and links to
    permissions per user.
    """
    lock_owner = models.ForeignKey(
        User,
        help_text='User ID who owns the lock',
        null=False,
        on_delete=models.CASCADE,
    )

    address = models.CharField(
        help_text='Address of the home where the lock is',
        max_length=400,
        default='N/A'
    )

    def __str__(self):
        return 'Lock {} at {}'.format(self.id, str(self.address))


class Permission(models.Model):
    """
    Database model representing the 'permissions' that a given visitor has to 
    access a lock.
    """
    visitor = models.ForeignKey(
        Visitor,
        help_text='User that permissions are for',
        null=False,
        on_delete=models.CASCADE
    )

    lock = models.ForeignKey(
        Lock,
        help_text='Lock that the permissions act on',
        null=False,
        on_delete=models.CASCADE
    )

    allowed_access_general = models.BooleanField(
        help_text='Is the user allowed to open the lock?',
        default=False
    )

    time_start = models.TimeField(
        help_text='At what time can the user open the lock every day?',
    )

    time_end = models.TimeField(
        help_text='Until what time can the user open the lock?',
    )


class VisitorImage(models.Model):
    """
    Database model representing an image captured of a user from the lock's 
    camera. It associates an image (basically just bytes) with a row in the 
    User table. The user entry can be null, however, for unidentified users.
    """
    image = models.BinaryField(
        help_text='Image of the user, in bytes',
        editable=True
    )

    filename = models.CharField(
        help_text='Name of the file to deliver the bytes as',
        max_length=200
    )

    visitor = models.ForeignKey(
        Visitor,
        on_delete=models.SET_NULL,
        null=True
    )

    lock = models.ForeignKey(
        Lock,
        on_delete=models.CASCADE,
        null=True
    )

    image_datetime = models.DateTimeField(
        help_text='Date and time the image was captured'
    )


class Event(models.Model):
    timestamp = models.TimeField(
        help_text='Time that the event happened',
        auto_now=True
    )

    duration = models.IntegerField(
        help_text='Number of seconds that the event occurred for'
    )

    lock = models.ForeignKey(
        Lock,
        on_delete=models.CASCADE,
        help_text='Lock where the event occurred'
    )

    event_type = models.CharField(
        help_text='String representing the type of event that occurred',
        max_length=200
    )


class StrangerReport(models.Model):
    """
        Database model representing a stranger report. It holds latitude
        and longitude of report and the datetime of the report.
    """

    latitude = models.FloatField(
        help_text="latitude of suspicious reporting"
    )

    longitude = models.FloatField(
        help_text="longitude of suspicious reporting"
    )

    stranger_report_time = models.DateTimeField(
        default=datetime.now,
        help_text='Date and time the report was made'
    )

    lock = models.ForeignKey(
        Lock,
        on_delete=models.CASCADE
    )

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
