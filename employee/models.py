from django.db import models
from django.db import DatabaseError, transaction
from function.models import Function
from rank.models import Rank
from firm.models import Firm
from common.models import BaseUUIDModel, BaseHistoryModel
from common.constants import EMPLOYEE_CATEGORIE
import datetime
import http.client
import json
from common.constants import ENDPOINT_USER


class Employee(BaseUUIDModel):
    user = models.CharField(max_length=1000)
    matricule = models.CharField(max_length=50)
    category = models.IntegerField(choices=EMPLOYEE_CATEGORIE)
    rank = models.ForeignKey(Rank, on_delete=models.RESTRICT)
    functions = models.ManyToManyField(Function)

    def __str__(self):
        return self.matricule

    def insertHistory(employee: "Employee", user: str, operation: int):
        hemployee = HEmployee()
        hemployee.employee = employee
        hemployee.user1 = employee.user
        hemployee.matricule = employee.matricule
        hemployee.category = employee.category
        hemployee.rank = employee.rank
        hemployee.functions = employee.functions
        hemployee.is_active = employee.is_active
        hemployee.date = employee.date
        hemployee.operation = operation
        hemployee.user = user
        hemployee.save()

    @staticmethod
    def create(
        user1: str,
        category: int,
        rank: Rank,
        function: Function,
        user: str
    ):
        """ add employee """
        try:
            employee = Employee.objects.get(
                user=user1,
                function__service__branch__firm=function.service.branch.firm)
            employee.is_active = True
            employee.functions.clear()
        except Employee.DoesNotExist:
            employee = Employee()
            employee.user = user1
            fin = datetime.datetime.now().strftime("%m%Y")
            matricule = rank.firm.acronym + str(
                101 + len(
                    Employee.objects.select_for_update(
                        matricule__contains=fin
                    )
                )
            ) + "N" + fin
            employee.matricule = matricule
        employee.category = category
        employee.rank = rank
        employee.functions.add(function)
        employee.user = user

        try:
            with transaction.atomic():
                employee.save()

                Employee.insertHistory(
                    employee=employee, operation=1, user=user)
            return employee
        except DatabaseError:
            return None

    def change(
        self,
        category: int,
        rank: Rank,
        function: Function,
        user: str
    ):
        """ update employee """
        self.category = category
        self.rank = rank
        self.functions.add(function)
        self.user = user

        try:
            with transaction.atomic():
                self.save()
                Employee.insertHistory(employee=self, user=user, operation=2)
            return self
        except DatabaseError:
            return None

    def delete(self, user: str):
        """ delete employee """
        self.is_active = False

        try:
            with transaction.atomic():
                self.save()

                Employee.insertHistory(employee=self, operation=3, user=user)
            return self
        except DatabaseError:
            return None

    def restore(self, user: str):
        """ restore employee """
        self.is_active = True

        try:
            with transaction.atomic():
                self.save()
                Rank.insertHistory(rank=self, operation=4, user=user)
            return self
        except DatabaseError:
            return None

    def decryptuser(self, authorization: str):
        data = Employee.get_user(user=self.user, authorization=authorization)
        self.utilisateur = data
        return self

    @staticmethod
    def get_user(user: str, authorization: str):
        conn = http.client.HTTPSConnection(ENDPOINT_USER)
        payload = ''
        headers = {
            "Authorization": authorization
        }
        url = "/profil/" + user + "/"
        conn.request("GET", url, payload, headers)
        response = conn.getresponse()
        dat = response.read()
        data = json.loads(dat)
        return data if data.get('uuid', 0) != 0 else None

    @classmethod
    def readByToken(cls, token: str, is_change=False):
        """ take an employee from token"""
        if is_change is False:
            return cls.objects.get(id=token)
        return cls.objects.select_for_update().get(id=token)

    @staticmethod
    def firms_visibles(user: str, is_superuser=False):
        if is_superuser is True:
            return Firm.objects.all()
        else:
            employees = Employee.objects.filter(is_active=True, user=user)
            firms = []
            for employee in employees:
                if employee.rank.firm.is_active is True:
                    firms.append(employee.rank.firm)
            return firms

    @staticmethod
    def branchs_visibles(user: str, is_superuser=False):
        firms = Employee.firms_visibles(user=user, is_superuser=is_superuser)
        branchs = []
        for firm in firms:
            if is_superuser is True:
                all_firm_branch = firm.branchs.all()
            else:
                all_firm_branch = firm.branchs.filter(is_active=True)
            for item in all_firm_branch:
                branchs.append(item)
        return branchs

    @staticmethod
    def services_visibles(user: str, is_superuser=False):
        branchs = Employee.branchs_visibles(
            user=user, is_superuser=is_superuser
        )
        services = []
        for branch in branchs:
            try:
                service = branch.service
                if is_superuser is True:
                    services.append(service)
                elif service.is_active is True:
                    services.append(service)
            except AttributeError:
                pass
        return services

    @staticmethod
    def functions_visibles(user: str, is_superuser=False):
        if is_superuser is True:
            return Function.objects.all()
        else:
            services = Employee.services_visibles(user=user)
            functions = []
            for service in services:
                for function in service.functions.filter(is_active=True):
                    functions.append(function)
        return functions


class HEmployee(BaseHistoryModel):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.RESTRICT,
        related_name="hemployees"
    )
    matricule = models.CharField(max_length=50)
    user1 = models.CharField(max_length=1000)
    category = models.IntegerField(choices=EMPLOYEE_CATEGORIE)
    rank = models.ForeignKey(Rank, on_delete=models.RESTRICT)
    functions = models.ManyToManyField(Function)
