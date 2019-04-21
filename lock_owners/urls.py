from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns

from lock_owners.views import (EventCreateView, EventDetailView,
                               LockCreateView, LockDetailView, OwnerCreateView,
                               OwnerDetailView, PermissionCreateView,
                               PermissionDetailView, StrangerReportView,
                               TempAuthCreateView, TempAuthDetailView,
                               ResidentCreateView, ResidentDetailView,
                               ResidentImageCreateView, ResidentImageDetailView,
                               VisitorImageView, create_img_template,
                               get_auth_code_for_id, get_events_for_lock,
                               get_temp_auth_id_for_visitor_and_lock,
                               get_user_id_for_token,
                               verify_auth_code, get_temp_auths_for_lock, 
                               get_locks_for_owner, get_events_for_user, 
                               get_residents_for_lock, get_residents_for_owner,
                               send_text, reply)

app_name = 'lock_owners'

urlpatterns = [
    url(r'^api/owners/$', OwnerCreateView.as_view()),
    url(r'^api/owners/(?P<pk>[0-9]+)/$', OwnerDetailView.as_view()),
    url(r'^api/locks/$', LockCreateView.as_view()),
    url(r'^api/locks/(?P<pk>[0-9]+)/$', LockDetailView.as_view()),
    url(r'^api/locks/owner/', get_locks_for_owner),
    url(r'^api/permissions/', PermissionCreateView.as_view()),
    url(r'^api/permissions/(?P<pk>[0-9]+)/$', PermissionDetailView.as_view()),
    url(r'^api/events/$', EventCreateView.as_view()),
    url(r'^api/events/(?P<pk>[0-9]+)/$', EventDetailView.as_view()),
    url(r'^api/events/user/$', get_events_for_user),
    url(r'^api/events/lock/(?P<id>[0-9]+)/$', get_events_for_lock),
    url(r'^api/residents/$', ResidentCreateView.as_view()),
    url(r'^api/residents/(?P<pk>[0-9]+)/$', ResidentDetailView.as_view()),
    url(r'^api/residents/lock/', get_residents_for_lock),
    url(r'^api/residents/owner/', get_residents_for_owner),
    url(r'^api/resident-images/', ResidentImageCreateView.as_view()),
    url(r'^api/resident-images/(?P<pk>[0-9]+)/$',
        ResidentImageDetailView.as_view()),
    url(r'^api/srn/$', StrangerReportView.as_view()),
    url(r'^api/post_image/$', VisitorImageView),
    url(r'^api/image/$', create_img_template),
    url(r'^api/notify/$', send_text),
    url(r'^api/teamedward/$', reply),
    url(r'^api/authenticate/$', obtain_auth_token),
    url(r'^api/temp_auth/$', TempAuthCreateView.as_view()),
    url(r'^api/temp_auth/(?P<pk>[0-9]+)/$', TempAuthDetailView.as_view()),
    url(r'^api/temp_auth/verify/$', verify_auth_code),
    url(r'^api/temp_auth/get_id/$', get_temp_auth_id_for_visitor_and_lock),
    url(r'^api/temp_auth/get_code/$', get_auth_code_for_id),
    url(r'^api/temp_auth/lock/$', get_temp_auths_for_lock),
    url(r'^api/authenticate/get_user_id/', get_user_id_for_token)
]

urlpatterns = format_suffix_patterns(urlpatterns)
