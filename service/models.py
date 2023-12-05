from django.db import models
from django.db import DatabaseError, transaction
from simple_history.models import HistoricalRecords
from common.models import BaseUUIDModel
from branch.models import Branch
import json
from datetime import datetime

# Create your models here.


class Service(BaseUUIDModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    branch = models.OneToOneField(
        Branch, on_delete=models.RESTRICT, related_name="service")
    history = HistoricalRecords()

    class Meta:
        """ defined how the data will be shouted into the database """
        ordering = ["name"]

    def __str__(self):
        return "%s" % self.name

    @staticmethod
    def create(name: str, description: str, branch: Branch, user: str):
        """ add service """
        try:
            service = Service.objects.get(
                name=name.upper(), branch__firm=branch.firm)
        except Service.DoesNotExist:
            service = Service()
            service.name = name.upper()
        service.description = description
        service.branch = branch
        service.is_active = True

        try:
            with transaction.atomic():
                service._change_reason = json.dumps({
                    "reason": "Add a new service",
                    "user": user
                })
                service._history_date = datetime.now()
                service.save()
                service.branch.changeIsService(user=user, is_service=True)
                service.branch.save()
            return service
        except DatabaseError:
            return None

    def change(self, name: str, description: str, branch: Branch, user: str):
        """ update service """
        self.name = name.upper()
        self.description = description
        self.branch = branch

        try:
            with transaction.atomic():
                self._change_reason = json.dumps({
                    "reason": "Update a service",
                    "user": user
                })
                self._history_date = datetime.now()
                self.save()

                self.branch.changeIsService(user=user, is_service=True)
                self.branch.save()
            return self
        except DatabaseError:
            return None

    def delete(self, user: str):
        """ delete service """
        self.is_active = False

        try:
            with transaction.atomic():
                self._change_reason = json.dumps({
                    "reason": "Delete a service",
                    "user": user
                })
                self._history_date = datetime.now()
                self.save()

                self.branch.changeIsService(user=user, is_service=False)
                self.branch.save()
            return self
        except DatabaseError:
            return None

    def restore(self, user: str):
        """ restore service """
        self.is_active = True

        try:
            with transaction.atomic():
                self._change_reason = json.dumps({
                    "reason": "Restore a service",
                    "user": user
                })
                self._history_date = datetime.now()
                self.save()

                self.branch.changeIsService(user=user, is_service=True)
                self.branch.save()
            return self
        except DatabaseError:
            return None
