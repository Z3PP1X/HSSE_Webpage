from django.db import models
import uuid
from django.contrib.auth import get_user_model


class Table(models.Model):

    sys_id = models.UUIDField(default=uuid.uuid4,
                                editable=False,
                                unique=True,
                                primary_key=True)

    created_by = models.ForeignKey(
        get_user_model(),
        related_name='created_%(class)s_set',
        on_delete=models.SET_NULL,
        null=True, editable=False)

    updated_by = models.ForeignKey(
        get_user_model(),
        related_name='updated_%(class)s_set',
        on_delete=models.SET_NULL,
        null=True, editable=False)

    updated_on = models.DateTimeField(auto_now=True, editable=False)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        abstract = True