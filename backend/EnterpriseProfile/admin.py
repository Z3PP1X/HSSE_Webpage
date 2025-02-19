from django.contrib import admin
from .models import BranchNetwork
from Core.admin import TableAdmin

# Register your models here.

class BranchNetworkAdmin(TableAdmin):

    """Define the admin page for the branch network model."""

    list_display = ('sys_id', 'created_on', 'created_by', 'CostCenter', 'BranchName')

admin.site.register(BranchNetwork, BranchNetworkAdmin)

