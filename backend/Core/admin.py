"""
Django admin customisation
"""
from django.contrib import admin
from django.utils import timezone
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from User import models


class TableAdmin(admin.ModelAdmin):
    """Define readonly fields for all models."""

    readonly_fields = ['created_by', 'updated_by', 'updated_on', 'created_on']

    def save_model(self, request, obj, form, change):
        """Set the created_by and updated_by fields to the current user."""
        if not obj.pk:
            obj.created_by = request.user
            obj.created_on = timezone.now()
        obj.updated_by = request.user
        obj.updated_on = timezone.now()
        super().save_model(request, obj, form, change)

    list_filter = ('created_by', 'updated_by', 'updated_on', 'created_on')
    search_fields = ('created_by', 'updated_by', 'updated_on', 'created_on')


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
                )
        }),
    )


admin.site.register(models.User, UserAdmin)
