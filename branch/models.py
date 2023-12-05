from django.db import models
from simple_history.models import HistoricalRecords

from common.models import BaseUUIDModel
import json
from datetime import datetime

from firm.models import Firm


class Branch(BaseUUIDModel):
    firm = models.ForeignKey(
        Firm, on_delete=models.RESTRICT, related_name="branchs")
    label = models.CharField(max_length=100)
    origin = models.ForeignKey(
        "Branch",
        on_delete=models.RESTRICT, null=True)
    is_principal = models.BooleanField(default=False)
    is_service = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.label

    class Meta:
        """ defined how the data will be shouted into the database """
        ordering = ["is_principal", "label", "date"]

    @staticmethod
    def create(
        label: str,
        firm: Firm,
        origin: "Branch",
        is_principal: bool,
        user: str
    ):
        """ add branch """
        branch = Branch()
        branch.label = label.upper()
        branch.firm = firm
        if is_principal is False:
            branch.origin = origin
        branch.is_principal = is_principal
        branch._change_reason = json.dumps({
            "reason": "Add a new branch",
            "user": user
        })
        branch._history_date = datetime.now()
        branch.save()
        return branch

    def change(self, label: str, origin: "Branch", user: str):
        """ update branch"""
        self.label = label.upper()
        self.origin = origin
        self.user = user

        self._change_reason = json.dumps({
            "reason": "Update a branch",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def delete(self, user: str):
        self.is_active = False

        self._change_reason = json.dumps({
            "reason": "Delete a branch",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()

    def restore(self, user: str):
        self.is_active = True
        self._change_reason = json.dumps({
            "reason": "Restore a branch",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()

    def changeIsService(self, user: str, is_service: bool):
        self.is_service = is_service
        texte = "Add a service to a branch" if is_service is True else "Remove a service to a branch"
        self._change_reason = json.dumps({
            "reason": texte,
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self
