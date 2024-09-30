from django.db import models
import uuid
from django.contrib.auth.models import User
from middleware.currentUser import get_current_user


class Table(models.Model):

    sys_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_by = models.ForeignKey(
        User,
        related_name='created_%(class)s_set',
        on_delete=models.SET_NULL,
        null=True, editable=False
        )
    updated_by = models.ForeignKey(
        User,
        related_name='updated_%(class)s_set',
        on_delete=models.SET_NULL,
        null=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=False)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        current_user = get_current_user()
        if not self.pk and current_user:
            self.created_by = current_user
        if current_user:
            self.updated_by = current_user
        super().save(*args, **kwargs)

        