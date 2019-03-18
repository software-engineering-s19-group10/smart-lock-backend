from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from lock_owners.views import UserCreateView, UserDetailView
from lock_owners.views import LockCreateView, LockDetailView
from lock_owners.views import PermissionCreateView, PermissionDetailView, StrangerReportView, send_mms, send_text

app_name = 'lock_owners'

urlpatterns = [
    url(r'^api/users/$', UserCreateView.as_view()),
    url(r'^api/users/(?P<pk>[0-9]+)/$', UserDetailView.as_view()),
    url(r'^api/locks/', LockCreateView.as_view()),
    url(r'^api/locks/(?P<pk>[0-9]+)/$', LockDetailView.as_view()),
    url(r'^api/permissions/', PermissionCreateView.as_view()),
    url(r'^api/permissions/(?P<pk>[0-9]+)/$', PermissionDetailView.as_view()),
    url(r'^api/srn/$', StrangerReportView.as_view()),
    url(r'^api/mms/$', send_mms),
    url(r'^api/sms/$', send_text)
]

urlpatterns = format_suffix_patterns(urlpatterns)