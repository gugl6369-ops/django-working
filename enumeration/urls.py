from django.urls import path, include, re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.index,  name='index'),
    re_path(r'^application/$', views.ApplicationList.as_view(), name='application_list'),
    re_path(r'^my-applications/$', views.MyApplicationList.as_view(), name='my_applications'),
    re_path(r'^applications/(?P<pk>\d+)/delete/$', views.ApplicationDelete.as_view(), name='application-delete'),
    re_path(r'^my-applications/create/$', views.ApplicationAdd.as_view(), name='application_create'),
    re_path(r'^registration/$', views.consumer_login, name='registration'),
]

