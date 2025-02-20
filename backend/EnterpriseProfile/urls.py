""""
URL Mappings for the Branch Network app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('branchnetwork', views.BranchRecordViewSet)

app_name = 'branchnetwork'

urlpatterns = [
    path('', include(router.urls)),
]
