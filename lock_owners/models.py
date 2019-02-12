from django.db import models

# Create your models here.
class User(models.Model):
    """
    Database model for a user of our system. A user is just someone who uses 
    the system.
    """
    username = models.CharField(
        help_text='Username of user (max length: 100 characters)',
        max_length=100
    )

    full_name = models.CharField(
        help_text='Full name of the user',
        max_length=200
    )

    phone = models.CharField(
        help_text='User phone number (no spaces or dashes, 10 character max)',
        max_length=10
    )

    email = models.EmailField(
        help_text='User email address'
    )

    def __str__(self):
        return '{} ({})'.format(str(self.full_name), str(self.username))  


class Owner(models.Model):
    """
    Database model for the owner of a lock. Directly links to user for basic 
    info, but with a few added fields.
    """
    user = models.ForeignKey(
        User,
        help_text='User ID of the owner',
        null=False,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(User.objects.get(id=self.user))


class Lock(models.Model):
    """
    Database model for a smart lock. Contains useful info and links to
    permissions per user.
    """
    lock_owner = models.ForeignKey(
        Owner,
        help_text='Owner ID of the lock',
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
    Database model representing the 'permissions' that a given user has to 
    access a lock. For now, it is just a boolean (is the user allowed to 
    unlock?) but it can be expanded later.
    """
    user = models.ForeignKey(
        User,
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
        auto_now=True
    )

    time_end = models.TimeField(
        help_text='Until what time can the user open the lock?',
        auto_now=True
    )