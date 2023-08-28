from django.db import models
from django.db import DatabaseError, transaction
from common.models import BaseHistoryModel, BaseUUIDModel

from service.models import Service


class Function(BaseUUIDModel):
    name = models.CharField(max_length=100)
    power = models.IntegerField()
    description = models.TextField()
    service = models.ForeignKey(
        Service,
        on_delete=models.RESTRICT,
        related_name="functions"
    )

    def __str__(self):
        return self.name

    def insertHistory(function: "Function", user: str, operation: int):
        hfunction = HFunction()
        hfunction.function = function
        hfunction.name = function.name
        hfunction.power = function.power
        hfunction.description = function.description
        hfunction.service = function.service
        hfunction.is_active = function.is_active
        hfunction.date = function.date
        hfunction.operation = operation
        hfunction.user = user
        hfunction.save()

    @staticmethod
    def create(
        name: str,
        power: int,
        description: str,
        service: Service,
        user: str
    ):
        """ add function """
        try:
            function = Function.objects.get(
                name=name.upper(),
                service__branch__firm=service.branch.firm)
        except Function.DoesNotExist:
            function = Function()
            function.name = name.upper()
        function.power = power
        function.description = description
        function.service = service
        function.is_active = True

        try:
            with transaction.atomic():
                function.save()

                Function.insertHistory(
                    function=function, operation=1, user=user)
            return function
        except DatabaseError:
            return None

    def change(
        self,
        name: str,
        power: int,
        description: str,
        service: Service,
        user: str
    ):
        """ update function """
        self.name = name.upper()
        self.power = power
        self.description = description
        self.service = service

        try:
            with transaction.atomic():
                self.save()
                Function.insertHistory(function=self, user=user, operation=2)
            return self
        except DatabaseError:
            return None

    def delete(self, user: str):
        """ delete function """
        self.is_active = False

        try:
            with transaction.atomic():
                self.save()

                Function.insertHistory(function=self, operation=3, user=user)
            return self
        except DatabaseError:
            return None

    def restore(self, user: str):
        """ restore function """
        self.is_active = True

        try:
            with transaction.atomic():
                self.save()
                Function.insertHistory(function=self, operation=4, user=user)
            return self
        except DatabaseError:
            return None

    @classmethod
    def readByToken(cls, token: str, is_change=False):
        """ take an function from token"""
        if is_change is False:
            return cls.objects.get(id=token)
        return cls.objects.select_for_update().get(id=token)


class HFunction(BaseHistoryModel):
    function = models.ForeignKey(
        Function,
        on_delete=models.RESTRICT,
        related_name="hfunctions",
        editable=False
    )
    name = models.CharField(max_length=100, editable=False)
    power = models.IntegerField(editable=False)
    description = models.TextField(editable=False)
    service = models.ForeignKey(
        Service,
        on_delete=models.RESTRICT,
    )
