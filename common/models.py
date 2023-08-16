import uuid as uuid
from django.db import models
from common.constants import H_OPERATION_CHOICE


class BaseUUIDModel(models.Model):
    """
    Base UUID model that represents a unique identifier for a given model.
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, db_index=True, editable=False)
    is_active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, editable=False)

    class Meta:
        abstract = True


class BaseHistoryModel(models.Model):
    """
    Base History model that add specific attributs for a given model.
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, db_index=True, editable=False)
    is_active = models.BooleanField(default=True, editable=False)
    date = models.DateTimeField(editable=False)
    operation = models.IntegerField(choices=H_OPERATION_CHOICE, editable=False)
    user = models.CharField(editable=False, max_length=1000)
    dateop = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        abstract = True
