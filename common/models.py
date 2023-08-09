import uuid as uuid
from django.db import models


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
