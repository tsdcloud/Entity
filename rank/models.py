from django.db import models
from django.db import DatabaseError, transaction
from common.models import BaseHistoryModel, BaseUUIDModel

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

    def __str__(self):
        return self.label

    def insertHistory(rank: "Rank", user: str, operation: int):
        hrank = HRank()
        hrank.rank = rank
        hrank.label = rank.label
        hrank.power = rank.power
        hrank.firm = rank.firm
        hrank.is_active = rank.is_active
        hrank.date = rank.date
        hrank.operation = operation
        hrank.user = user
        hrank.save()

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

        try:
            with transaction.atomic():
                rank.save()

                Rank.insertHistory(
                    rank=rank, operation=1, user=user)
            return rank
        except DatabaseError:
            return None

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

        try:
            with transaction.atomic():
                self.save()
                Rank.insertHistory(rank=self, user=user, operation=2)
            return self
        except DatabaseError:
            return None

    def delete(self, user: str):
        """ delete rank """
        self.is_active = False

        try:
            with transaction.atomic():
                self.save()

                Rank.insertHistory(rank=self, operation=3, user=user)
            return self
        except DatabaseError:
            return None

    def restore(self, user: str):
        """ restore rank """
        self.is_active = True

        try:
            with transaction.atomic():
                self.save()
                Rank.insertHistory(rank=self, operation=4, user=user)
            return self
        except DatabaseError:
            return None

    @classmethod
    def readByToken(cls, token: str, is_change=False):
        """ take an rank from token"""
        if is_change is False:
            return cls.objects.get(id=token)
        return cls.objects.select_for_update().get(id=token)


class HRank(BaseHistoryModel):
    rank = models.ForeignKey(
        Rank,
        on_delete=models.RESTRICT, related_name="hranks")
    label = models.CharField(max_length=100)
    power = models.IntegerField()
    firm = models.ForeignKey(Firm, on_delete=models.RESTRICT)
