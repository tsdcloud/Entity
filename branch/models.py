from django.db import models
from django.db import DatabaseError, transaction
import uuid

from firm.models import Firm

from common.constances import HOPERATION_CHOICE

# Create your models here.
class Branch(models.Model):
    """ branchs management """
    uuid = models.CharField(max_length=1000,editable=False)
    libelle = models.CharField(default="unknow", max_length=100, editable=False)
    firm = models.ForeignKey(Firm, on_delete=models.RESTRICT, related_name="branchs" , editable=False)
    origine = models.CharField(default="start", max_length=1000, editable=False)
    principal = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        """ defined how the data will be shouted into the database """
        ordering = ["principal", "libelle", "date"]

    def __str__(self):
        """ name in the administration """
        return self.libelle + "(" + self.principale + ")" + " " + self.firm.social_raison

    @staticmethod
    def create(libelle:str, firm:Firm, origine:str, principal:bool, user:str):
        """ add branch """
        branch = Branch()
        branch.uuid = str(uuid.uuid4())
        branch.libelle = libelle.upper()
        branch.firm = firm
        branch.origine = origine
        branch.principal = principal
       

        hbranch = HBranch()

        try:
            with transaction.atomic():
                branch.save()

                branch.uuid += ':' + str(branch.pk)

                branch.save()

                hbranch.branch = branch
                hbranch.uuid = branch.uuid 
                hbranch.libelle = branch.libelle
                hbranch.firm = branch.firm
                hbranch.origine = branch.origine 
                hbranch.principal = branch.principal
                hbranch.active = branch.active
                hbranch.date = branch.date 
                hbranch.operation = 1
                hbranch.user= user

                hbranch.save()
                
            return branch
        except DatabaseError:
            return None

    @classmethod
    def readByToken(cls,token:str):
        return cls.objects.get(uuid=token)

class HBranch(models.Model):
    """ historiques des mise a jour des branches """
    branch = models.ForeignKey(Branch, on_delete=models.RESTRICT, related_name="hbranchs" , editable=False)
    uuid = models.CharField(max_length=1000,editable=False)
    libelle = models.CharField(default="inconnue", max_length=10, editable=False)
    firm = models.ForeignKey(Firm, on_delete=models.RESTRICT, related_name="hbranchs" , editable=False)
    origine = models.CharField(default="start", max_length=1000, editable=False)
    principal = models.BooleanField(default=True, editable=False)
    active = models.BooleanField(default=True, editable=False)
    date = models.DateTimeField(editable=False)
    operation = models.IntegerField(choices=HOPERATION_CHOICE, editable=False)
    user = models.CharField(editable=False, max_length=1000)
    dateop = models.DateTimeField(auto_now_add=True, editable=False)