""""
URL Mappings for the recipe app.
"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('firstaidrecord', views.FirstAidRecordViewSet)

app_name = 'digitalfirstaid'

urlpatterns = [
    path('', include(router.urls)),

]
