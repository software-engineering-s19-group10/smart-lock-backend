from django.contrib import admin
from lock_owners.models import Owner, Lock, Visitor, Permission, VisitorImage, Event, StrangerReport, TempAuth

# Register your models here.
admin.site.register(Owner)
admin.site.register(Lock)
admin.site.register(Visitor)
admin.site.register(Permission)
admin.site.register(VisitorImage)
admin.site.register(Event)
admin.site.register(StrangerReport)
admin.site.register(TempAuth)