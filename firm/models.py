from django.db import models
from django.db import DatabaseError, transaction

from common.models import BaseUUIDModel
from common.constants import H_OPERATION_CHOICE
from . constants import TAX_SYSTEM, TYPE_PERSON

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
        max_length=18
    )
    logo = models.TextField()
    type_person = models.IntegerField(choices=TYPE_PERSON)

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
        firm = Firm()
        firm.business_name = business_name.upper()
        firm.acronym = acronym.upper()
        firm.unique_identifier_number = unique_identifier_number.upper()
        firm.principal_activity = principal_activity.upper()
        firm.regime = regime
        firm.tax_reporting_center = tax_reporting_center.upper()
        firm.trade_register = trade_register.upper()
        firm.logo = logo
        firm.type_person = type_person

        hfirm = HFirm()

        try:
            with transaction.atomic():
                firm.save()

                hfirm.firm = firm
                hfirm.business_name = firm.business_name
                hfirm.acronym = firm.acronym
                hfirm.unique_identifier_number = firm.unique_identifier_number
                hfirm.principal_activity = firm.principal_activity
                hfirm.regime = firm.regime
                hfirm.tax_reporting_center = firm.tax_reporting_center
                hfirm.trade_register = firm.trade_register
                hfirm.logo = firm.logo
                hfirm.type_person = firm.type_person
                hfirm.is_active = firm.is_active
                hfirm.date = firm.date
                hfirm.operation = 1
                hfirm.user = user

                hfirm.save()
            return firm
        except DatabaseError:
            return None

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

        hfirm = HFirm()

        try:
            with transaction.atomic():
                self.save()

                hfirm.firm = self
                hfirm.business_name = self.business_name
                hfirm.acronym = self.acronym
                hfirm.unique_identifier_number = self.unique_identifier_number
                hfirm.principal_activity = self.principal_activity
                hfirm.regime = self.regime
                hfirm.tax_reporting_center = self.tax_reporting_center
                hfirm.trade_register = self.trade_register
                hfirm.logo = self.logo
                hfirm.type_person = self.type_person
                hfirm.is_active = self.is_active
                hfirm.date = self.date
                hfirm.operation = 2
                hfirm.user = user

                hfirm.save()

            return self
        except DatabaseError:
            return None

    def delete(self, user: str):
        """ delete entity """
        self.is_active = False

        hfirm = HFirm()

        try:
            with transaction.atomic():
                self.save()

                hfirm.firm = self
                hfirm.business_name = self.business_name
                hfirm.acronym = self.acronym
                hfirm.unique_identifier_number = self.unique_identifier_number
                hfirm.principal_activity = self.principal_activity
                hfirm.regime = self.regime
                hfirm.tax_reporting_center = self.tax_reporting_center
                hfirm.trade_register = self.trade_register
                hfirm.logo = self.logo
                hfirm.type_person = self.type_person
                hfirm.is_active = self.is_active
                hfirm.date = self.date
                hfirm.operation = 3
                hfirm.user = user

                hfirm.save()

            return self
        except DatabaseError:
            return None

    def restore(self, user: str):
        """ active entity previously disabled """
        self.is_active = True

        hfirm = HFirm()

        try:
            with transaction.atomic():
                self.save()

                hfirm.firm = self
                hfirm.business_name = self.business_name
                hfirm.acronym = self.acronym
                hfirm.unique_identifier_number = self.unique_identifier_number
                hfirm.principal_activity = self.principal_activity
                hfirm.regime = self.regime
                hfirm.tax_reporting_center = self.tax_reporting_center
                hfirm.trade_register = self.trade_register
                hfirm.logo = self.logo
                hfirm.type_person = self.type_person
                hfirm.is_active = self.is_active
                hfirm.date = self.date
                hfirm.operation = 4
                hfirm.user = user

                hfirm.save()

            return self
        except DatabaseError:
            return None

    @classmethod
    def readByToken(cls, token: str):
        """ take an entity from token"""
        return cls.objects.get(uuid=token)


class HFirm(models.Model):
    """ firm history """
    firm = models.ForeignKey(
        Firm, on_delete=models.RESTRICT, related_name="hfirm", editable=False)
    business_name = models.CharField(
        verbose_name="Business Name",
        unique=True, max_length=100, editable=False)
    acronym = models.CharField(max_length=20, editable=False)
    unique_identifier_number = models.CharField(
        verbose_name="Unique Identifier Number",
        unique=True, max_length=14, editable=False)
    principal_activity = models.CharField(
        verbose_name="Principal Activity",
        max_length=150, editable=False)
    regime = models.IntegerField(choices=TAX_SYSTEM, editable=False)
    tax_reporting_center = models.CharField(
        verbose_name="Tax Reporting Center",
        max_length=50, editable=False)
    trade_register = models.CharField(
        verbose_name="Trade Register",
        unique=True, max_length=18, editable=False)
    logo = models.TextField(editable=False)
    type_person = models.IntegerField(choices=TYPE_PERSON, editable=False)
    is_active = models.BooleanField(default=True, editable=False)
    date = models.DateTimeField(editable=False)
    operation = models.IntegerField(choices=H_OPERATION_CHOICE, editable=False)
    user = models.CharField(editable=False, max_length=1000)
    dateop = models.DateTimeField(auto_now_add=True, editable=False)
