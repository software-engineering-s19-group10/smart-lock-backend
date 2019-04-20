from django.contrib import admin

from lock_owners.models import (Event, Lock, Owner, Permission, StrangerReport,
                                TempAuth, Resident)

# Register your models here.
admin.site.register(Owner)
admin.site.register(Lock)
admin.site.register(Permission)
admin.site.register(Event)
admin.site.register(StrangerReport)
admin.site.register(TempAuth)
admin.site.register(Resident)
