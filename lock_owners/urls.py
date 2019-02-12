from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from lock_owners.views import UserCreateView, UserDetailView
from lock_owners.views import OwnerCreateView, OwnerDetailView


app_name = 'lock_owners'

urlpatterns = [
    url(r'^api/users/$', UserCreateView.as_view()),
    url(r'^api/users/(?P<pk>[0-9]+)/$', UserDetailView.as_view()),
    url(r'^api/owners/$', OwnerCreateView.as_view()),
    url(r'^api/owners/(?P<pk>[0-9]+)/$', OwnerDetailView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)