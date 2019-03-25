from django.contrib import admin
from lock_owners.models import User, Lock, Visitor, Permission, VisitorImage, Event, StrangerReport

# Register your models here.
admin.site.register(User)
admin.site.register(Lock)
admin.site.register(Visitor)
admin.site.register(Permission)
admin.site.register(VisitorImage)
admin.site.register(Event)
admin.site.register(StrangerReport)