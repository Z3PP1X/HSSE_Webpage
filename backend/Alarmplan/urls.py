""""
URL mappings for the Alarmplan API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('alarmplan', views.AlarmplanViewSet)

app_name = 'Alarmplan'

urlpatterns = [
    path('', include(router.urls)),
]