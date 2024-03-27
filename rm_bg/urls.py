from rm_bg import views
from django.urls import path

urlpatterns = [
    path('', views.process_image, name='rm.pg'),
]
