from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('setsensor', views.set_sensor, name='set_sensor'),
    path('addinfo', views.add_info, name='add_info'),
    path('updatevideo', views.update_video, name='update_video'),
]
