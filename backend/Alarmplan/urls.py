""""
URL mappings for the Alarmplan API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# Only register the combined approach
router.register('alarmplan', views.AlarmplanViewSet)
router.register('emergency-planning', views.EmergencyPlanningViewSet, basename='emergency-planning')

app_name = 'Alarmplan'

urlpatterns = [
    path('', include(router.urls)),
]
