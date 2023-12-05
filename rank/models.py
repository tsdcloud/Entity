from django.db import models
from common.models import BaseUUIDModel
from simple_history.models import HistoricalRecords
import json
from datetime import datetime

# Create your models here.
from firm.models import Firm


class Rank(BaseUUIDModel):
    label = models.CharField(max_length=150)
    power = models.IntegerField()
    firm = models.ForeignKey(
        Firm,
        on_delete=models.RESTRICT,
        related_name="ranks"
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.label

    @staticmethod
    def create(
        label: str,
        power: int,
        firm: Firm,
        user: str
    ):
        """ add rank """
        try:
            rank = Rank.objects.get(
                label=label.upper(),
                firm=firm
            )
        except Rank.DoesNotExist:
            rank = Rank()
            rank.label = label.upper()
        rank.power = power
        rank.firm = firm
        rank.is_active = True

        rank._change_reason = json.dumps({
            "reason": "Add a new rank",
            "user": user
        })
        rank._history_date = datetime.now()
        rank.save()
        return rank

    def change(
        self,
        label: str,
        power: int,
        user: str
    ):
        """ update rank """
        self.label = label.upper()
        self.power = power
        self.user = user

        self._change_reason = json.dumps({
            "reason": "Update rank",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def delete(self, user: str):
        """ delete rank """
        self.is_active = False

        self._change_reason = json.dumps({
            "reason": "Delete rank",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def restore(self, user: str):
        """ restore rank """
        self.is_active = True

        self._change_reason = json.dumps({
            "reason": "Restore rank",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self
