from django.contrib import admin
from lock_owners.models import User, Lock, Permission, UserImage

# Register your models here.
admin.site.register(User)
admin.site.register(Lock)
admin.site.register(Permission)
admin.site.register(UserImage)