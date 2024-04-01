from django.db import models
from simple_history.models import HistoricalRecords
from common.models import BaseUUIDModel
from . constants import TAX_SYSTEM, TYPE_PERSON
import json
from datetime import datetime

# Create your models here.


class Firm(BaseUUIDModel):
    """ Firm's class purpose is to manage entities """
    business_name = models.CharField(
        verbose_name="Business Name",
        unique=True,
        max_length=100
    )
    acronym = models.CharField(max_length=20)
    unique_identifier_number = models.CharField(
        verbose_name="Unique Identifier Number",
        unique=True,
        max_length=14
    )
    principal_activity = models.CharField(
        verbose_name="Principal Activity",
        max_length=150
    )
    regime = models.IntegerField(choices=TAX_SYSTEM)
    tax_reporting_center = models.CharField(
        verbose_name="Tax Reporting Center",
        max_length=50
    )
    trade_register = models.CharField(
        verbose_name="Trade Register",
        unique=True,
        max_length=50
    )
    logo = models.TextField()
    type_person = models.IntegerField(choices=TYPE_PERSON)
    history = HistoricalRecords()

    class Meta:
        """ defined how the data will be shouted into the database """
        ordering = ["business_name", "acronym", "date"]

    def __str__(self):
        """ name in the administration """
        return "(%s %s)" % (self.business_name, self.acronym)

    @staticmethod
    def create(
        business_name: str,
        acronym: str,
        unique_identifier_number: str,
        principal_activity: str,
        regime: str,
        tax_reporting_center: str,
        trade_register: str,
        logo: str,
        type_person: int,
        user: str
    ):
        """ add entity """
        try:
            firm = Firm.objects.get(business_name=business_name)
            firm.is_active = True
        except Firm.DoesNotExist:
            firm = Firm()
            firm.business_name = business_name.upper()

        firm.unique_identifier_number = unique_identifier_number.upper()
        firm.acronym = acronym.upper()
        firm.principal_activity = principal_activity.upper()
        firm.regime = regime
        firm.tax_reporting_center = tax_reporting_center.upper()
        firm.trade_register = trade_register.upper()
        firm.logo = logo
        firm.type_person = type_person
        firm._change_reason = json.dumps({
            "reason": "Add a new company",
            "user": user
        })
        firm._history_date = datetime.now()
        firm.save()
        return firm

    def change(
        self,
        business_name: str,
        acronym: str,
        unique_identifier_number: str,
        principal_activity: str,
        regime: str,
        tax_reporting_center: str,
        trade_register: str,
        logo: str,
        type_person: int,
        user: str
    ):
        """ change entity """
        self.business_name = business_name.upper()
        self.acronym = acronym.upper()
        self.unique_identifier_number = unique_identifier_number.upper()
        self.principal_activity = principal_activity.upper()
        self.regime = regime
        self.tax_reporting_center = tax_reporting_center.upper()
        self.trade_register = trade_register.upper()
        self.logo = logo
        self.type_person = type_person

        self._change_reason = json.dumps({
            "reason": "Update a company",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def delete(self, user: str):
        """ delete entity """
        self.is_active = False
        self._change_reason = json.dumps({
            "reason": "Delete a company",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def restore(self, user: str):
        """ active entity previously disabled """
        self.is_active = True

        self._change_reason = json.dumps({
            "reason": "Restore a company",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self
