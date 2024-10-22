from django.contrib import admin
from .models import FirstAidRecord
from Core.admin import TableAdmin


class FirstAidRecordAdmin(TableAdmin):
    """Define the admin page for the first aid record model."""

    list_display = ('sys_id', 'created_on', 'created_by')



admin.site.register(FirstAidRecord, FirstAidRecordAdmin)
