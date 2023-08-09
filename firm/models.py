import uuid

from django.db import models
from django.db import DatabaseError, transaction

from django.utils.translation import ugettext_lazy as _, get_language

from common.models import BaseUUIDModel
from common.constants import TAX_SYSTEM, TYPE_PERSON, H_OPERATION_CHOICE

# Create your models here.


class Firm(BaseUUIDModel):
    """ Firm's class purpose is to manage entities """
    business_name = models.CharField(_("Business Name"), unique=True, max_length=100)
    acronym = models.CharField(max_length=20)
    unique_identifier_number = models.CharField(_("Unique Identifier Number"), unique=True, max_length=14)
    principal_activity = models.CharField(_("Principal Activity"), max_length=150)
    regime = models.IntegerField(choices=TAX_SYSTEM)
    tax_reporting_center = models.CharField(_("Tax Reporting Center"), max_length=50)
    trade_register = models.CharField(_("Trade Register"), unique=True, max_length=18)
    logo = models.TextField()
    type_person = models.IntegerField(choices=TYPE_PERSON)

    class Meta:
        """ defined how the data will be shouted into the database """
        ordering = ["business_name", "acronym","date"]

    def __str__(self):
        """ name in the administration """
        return "(%s %s)" % (self.business_name, self.acronym)

    def create(business_name: str, acronym: str, niu: str, principal_activity: str, regime: str, tax_reporting_center: str, trade_register: str, logo: str, type_person: int, user:str):
        """ add entity """
        firm = Firm()
        firm.uuid = str(uuid.uuid4())
        firm.business_name = business_name.upper()
        firm.acronym = acronym.upper()
        firm.niu = niu.upper()
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

                firm.uuid += ':' + str(firm.pk)

                firm.save()

                hfirm.firm = firm
                hfirm.uuid = firm.uuid 
                hfirm.business_name = firm.business_name 
                hfirm.acronym = firm.acronym 
                hfirm.niu = firm.niu 
                hfirm.principal_activity = firm.principal_activity 
                hfirm.regime = firm.regime
                hfirm.tax_reporting_center = firm.tax_reporting_center 
                hfirm.trade_register = firm.trade_register 
                hfirm.logo = firm.logo 
                hfirm.type_person = firm.type_person 
                hfirm.active = firm.active 
                hfirm.date = firm.date 
                hfirm.operation = 1 
                hfirm.user = user

                hfirm.save()
                
            return firm
        except DatabaseError:
            return None
        
    create = staticmethod(create)

    @classmethod
    def readByToken(cls,token:str):
        """ take an entity from token"""
        return cls.objects.get(uuid=token)

class HFirm(models.Model):
    """ firm history """
    firm = models.ForeignKey(Firm, on_delete=models.RESTRICT, related_name="hfirme" , editable=False)
    uuid = models.CharField(max_length=1000,editable=False)
    business_name = models.CharField(default="inconnue", max_length=100,editable=False)
    acronym = models.CharField(default="inconnue", max_length=100, editable=False)
    niu = models.CharField(max_length=14, editable=False)
    principal_activity = models.CharField(max_length=150, editable=False)
    regime = models.IntegerField(choices=TAX_SYSTEM, editable=False)
    tax_reporting_center = models.CharField(max_length=50, editable=False)
    trade_register = models.CharField(max_length=18, editable=False)
    logo = models.TextField(default='e', editable=False)
    type_person = models.IntegerField(choices=TYPE_PERSON)
    active = models.BooleanField(default=True, editable=False)
    date = models.DateTimeField(editable=False)
    operation = models.IntegerField(choices=HOPERATION_CHOICE, editable=False)
    user = models.CharField(editable=False, max_length=1000)
    dateop = models.DateTimeField(auto_now_add=True, editable=False)