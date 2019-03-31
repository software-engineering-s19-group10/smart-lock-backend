from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns
from lock_owners.views import OwnerCreateView, OwnerDetailView
from lock_owners.views import LockCreateView, LockDetailView
from lock_owners.views import PermissionCreateView, PermissionDetailView, StrangerReportView, send_mms, send_text

from lock_owners.views import EventCreateView, EventDetailView
from lock_owners.views import get_events_for_lock

from lock_owners.views import (LockCreateView, LockDetailView,
                               PermissionCreateView, PermissionDetailView,
                               OwnerCreateView, OwnerDetailView)

app_name = 'lock_owners'

urlpatterns = [
    url(r'^api/owners/$', OwnerCreateView.as_view()),
    url(r'^api/owners/(?P<pk>[0-9]+)/$', OwnerDetailView.as_view()),
    url(r'^api/locks/', LockCreateView.as_view()),
    url(r'^api/locks/(?P<pk>[0-9]+)/$', LockDetailView.as_view()),
    url(r'^api/permissions/', PermissionCreateView.as_view()),
    url(r'^api/permissions/(?P<pk>[0-9]+)/$', PermissionDetailView.as_view()),
    url(r'^api/events/$', EventCreateView.as_view()),
    url(r'^api/events/(?P<pk>[0-9]+)/$', EventDetailView.as_view()),
    url(r'^api/events/lock/(?P<id>[0-9]+)/$', get_events_for_lock),
    url(r'^api/srn/$', StrangerReportView.as_view()),
    url(r'^api/sms/$', send_text),
    url(r'^api/mms/$', send_mms),
    url(r'^api/authenticate/$', obtain_auth_token),
]

urlpatterns = format_suffix_patterns(urlpatterns)
