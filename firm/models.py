from django.db import models
from django.db import DatabaseError, transaction
import uuid

from common.constances import HOPERATION_CHOICE
from .constances import TAX_SYSTEM, TYPE_PERSON

# Create your models here.
class Firm(models.Model):
    """ entities management """
    uuid = models.CharField(max_length=1000,editable=False)
    social_raison = models.CharField(verbose_name="social raison", unique=True, max_length=100)
    sigle = models.CharField(max_length=20)
    niu = models.CharField(unique=True, max_length=14)
    principal_activity = models.CharField(max_length=150, verbose_name="principal activity")
    regime = models.IntegerField(choices=TAX_SYSTEM)
    tax_reporting_center = models.CharField(max_length=50, verbose_name="centre de rattachement")
    trade_register = models.CharField(unique=True, verbose_name="registre de commerce", max_length=18)
    logo = models.TextField()
    type_person = models.IntegerField(choices=TYPE_PERSON)
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        """ defined how the data will be shouted into the database """
        ordering = ["social_raison", "sigle","date"]

    def __str__(self):
        """ name in the administration """
        return self.social_raison + "(" + self.sigle + ")"
    
    @staticmethod
    def create(social_raison: str, sigle: str, niu: str, principal_activity: str, regime: str, tax_reporting_center: str, trade_register: str, logo: str, type_person: int, user:str):
        """ add entity """
        firm = Firm()
        firm.uuid = str(uuid.uuid4())
        firm.social_raison = social_raison.upper()
        firm.sigle = sigle.upper()
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
                hfirm.social_raison = firm.social_raison 
                hfirm.sigle = firm.sigle 
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
    
    def change(self, social_raison: str, sigle: str, niu: str, principal_activity: str, regime: str, tax_reporting_center: str, trade_register: str, logo: str, type_person: int, user:str):
        """ change entity """
        self.social_raison = social_raison.upper()
        self.sigle = sigle.upper()
        self.niu = niu.upper()
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
                hfirm.uuid = self.uuid 
                hfirm.social_raison = self.social_raison 
                hfirm.sigle = self.sigle 
                hfirm.niu = self.niu 
                hfirm.principal_activity = self.principal_activity 
                hfirm.regime = self.regime
                hfirm.tax_reporting_center = self.tax_reporting_center 
                hfirm.trade_register = self.trade_register 
                hfirm.logo = self.logo 
                hfirm.type_person = self.type_person 
                hfirm.active = self.active 
                hfirm.date = self.date 
                hfirm.operation =  2
                hfirm.user = user

                hfirm.save()
                
            return self
        except DatabaseError:
            return None

    @classmethod
    def readByToken(cls,token:str):
        """ take an entity from token"""
        return cls.objects.get(uuid=token)

class HFirm(models.Model):
    """ firm history """
    firm = models.ForeignKey(Firm, on_delete=models.RESTRICT, related_name="hfirme" , editable=False)
    uuid = models.CharField(max_length=1000,editable=False)
    social_raison = models.CharField(default="inconnue", max_length=100,editable=False)
    sigle = models.CharField(default="inconnue", max_length=100, editable=False)
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