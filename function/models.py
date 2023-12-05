from django.db import models
from django.contrib.auth.models import Permission
from simple_history.models import HistoricalRecords
from common.models import BaseUUIDModel
import json
from datetime import datetime

from service.models import Service


class Function(BaseUUIDModel):
    name = models.CharField(max_length=100)
    power = models.IntegerField()
    description = models.TextField()
    service = models.ForeignKey(
        Service,
        on_delete=models.RESTRICT,
        related_name="functions"
    )
    permissions = models.ManyToManyField(Permission)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    @staticmethod
    def create(
        name: str,
        power: int,
        description: str,
        service: Service,
        user: str
    ):
        """ add function """
        try:
            function = Function.objects.get(
                name=name.upper(),
                service__branch__firm=service.branch.firm)
        except Function.DoesNotExist:
            function = Function()
            function.name = name.upper()
        function.power = power
        function.description = description
        function.service = service
        function.is_active = True

        function._change_reason = json.dumps({
            "reason": "Add a new function",
            "user": user
        })
        function._history_date = datetime.now()
        function.save()
        return function

    def change(
        self,
        name: str,
        power: int,
        description: str,
        service: Service,
        user: str
    ):
        """ update function """
        self.name = name.upper()
        self.power = power
        self.description = description
        self.service = service

        self._change_reason = json.dumps({
            "reason": "Update a function",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def delete(self, user: str):
        """ delete function """
        self.is_active = False

        self._change_reason = json.dumps({
            "reason": "Delete a function",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def restore(self, user: str):
        """ restore function """
        self.is_active = True

        self._change_reason = json.dumps({
            "reason": "Restore a function",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def add_permission(self, user: str, permissions):
        self.permissions.set(permissions)
        self._change_reason = json.dumps({
            "reason": "Update the permissions of function",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self
