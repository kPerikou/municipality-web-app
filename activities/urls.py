from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^registerDirector/$', views.register_director, name='registerDirector'),
    url(r'^registerDept/$', views.register_deptDirector, name='registerDept'),
    url(r'^registerOfficeClerk/$', views.register_officeClerk, name='registerOffice'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^home/$', views.homepage_view, name='home'),
    url(r'^info/$', views.info, name='info'),
    url(r'^myactivities/$', views.myactivities, name='myactivities'),
    url(r'^create_activity/$', views.create_activity, name='create_activity'),
    url(r'^create_task/$', views.create_task, name='create_task'),
    url(r'^notifications/$', views.notifications, name='notifications'),
    url(r'^show_activity/$', views.show_activity),
    url(r'^show_activity/(?P<activity_id>[0-9]+)$', views.show_activity, name='show_activity'),
    url(r'^show_activity_byNot/(?P<activity_id>[0-9]+)/(?P<notification_id>[0-9]+)$', views.show_activity_byNot, name='show_activity_byNot'),
    url(r'^progressProject/$', views.progressProject),
    url(r'^progressProject/(?P<project_id>[0-9]+)$', views.progressProject, name='progressProject'),
    path('create_project', views.create_project, name='create_project'),
    path('create_projectTask', views.create_projectTask, name='create_projectTask'),
    url(r'^submitTask/(?P<task_id>[0-9]+)$', views.submitTask, name='submitTask'),
    url(r'^approveTask/(?P<task_id>[0-9]+)$', views.approveTask, name='approveTask'),
    url(r'^rejectTask/(?P<task_id>[0-9]+)$', views.rejectTask, name='rejectTask'),
    url(r'^sendComment/$', views.sendComment, name='sendComment'),
]
