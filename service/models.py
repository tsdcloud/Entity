from django.db import models
from django.db import DatabaseError, transaction
from common.models import BaseUUIDModel, BaseHistoryModel
from branch.models import Branch

# Create your models here.


class Service(BaseUUIDModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    branch = models.OneToOneField(
        Branch, on_delete=models.RESTRICT, related_name="service")

    class Meta:
        """ defined how the data will be shouted into the database """
        ordering = ["name"]

    def __str__(self):
        return "%s" % self.name

    def insertHistory(service: "Service", user: str, operation: int):
        hservice = HService()
        hservice.service = service
        hservice.name = service.name
        hservice.description = service.description
        hservice.branch = service.branch
        hservice.is_active = service.is_active
        hservice.date = service.date
        hservice.operation = operation
        hservice.user = user
        hservice.save()

    @staticmethod
    def create(name: str, description: str, branch: Branch, user: str):
        """ add service """
        try:
            service = Service.objects.get(
                name=name.upper(), branch_firm=branch.firm)
        except Service.DoesNotExist:
            service = Service()
            service.name = name.upper()
        service.description = description
        service.branch = branch
        service.is_active = True

        try:
            with transaction.atomic():
                service.save()

                service.branch.changeIsService(user=user, is_service=True)
                service.branch.save()
                Service.insertHistory(service=service, operation=1, user=user)
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
                self.save()

                self.branch.is_service = True
                self.branch.save()

                Service.insertHistory(service=self, operation=2, user=user)
            return self
        except DatabaseError:
            return None

    def delete(self, user: str):
        """ delete service """
        self.is_active = False

        try:
            with transaction.atomic():
                self.save()

                self.branch.changeIsService(user=user, is_service=False)
                self.branch.save()

                Service.insertHistory(service=self, operation=3, user=user)
            return self
        except DatabaseError:
            return None

    def restore(self, user: str):
        """ restore service """
        self.is_active = True

        try:
            with transaction.atomic():
                self.save()

                self.branch.changeIsService(user=user, is_service=True)
                self.branch.save()

                Service.insertHistory(service=self, operation=4, user=user)
            return self
        except DatabaseError:
            return None

    @classmethod
    def readByToken(cls, token: str, is_change=False):
        """ take an service from token"""
        if is_change is False:
            return cls.objects.get(id=token)
        return cls.objects.select_for_update().get(id=token)


class HService(BaseHistoryModel):
    service = models.ForeignKey(
        Service, on_delete=models.RESTRICT, related_name="hservices")
    name = models.CharField(max_length=100)
    description = models.TextField()
    branch = models.ForeignKey(
        Branch, on_delete=models.RESTRICT, related_name="hservices")
