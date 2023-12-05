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
    __history_date = None

    @property
    def _history_date(self):
        return self.__history_date

    @_history_date.setter
    def _history_date(self, value):
        self.__history_date = value

    @classmethod
    def readByToken(cls, token: str, is_change=False):
        """ take an firm from token"""
        if is_change is False:
            return cls.objects.get(id=token)
        return cls.objects.select_for_update().get(id=token)

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
