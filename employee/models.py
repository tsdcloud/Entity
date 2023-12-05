from django.db import models
from django.contrib.auth.models import Permission
from function.models import Function
from rank.models import Rank
from firm.models import Firm
from location.models import (
    Location, Country, Region, Department, Municipality, Village, Portee, Link)
from common.models import BaseUUIDModel
from simple_history.models import HistoricalRecords
from common.constants import EMPLOYEE_CATEGORIE
from datetime import datetime
import http.client
import json
from common.constants import ENDPOINT_USER


class Employee(BaseUUIDModel):
    user = models.CharField(max_length=1000)
    matricule = models.CharField(max_length=50)
    category = models.IntegerField(choices=EMPLOYEE_CATEGORIE)
    rank = models.ForeignKey(Rank, on_delete=models.RESTRICT)
    functions = models.ManyToManyField(Function)
    permissions = models.ManyToManyField(Permission)
    history = HistoricalRecords()

    def __str__(self):
        return self.matricule

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
                functions__service__branch__firm=function.service.branch.firm)
            employee.is_active = True
            employee.functions.clear()
        except Employee.DoesNotExist:
            employee = Employee()
            employee.user = user1
            fin = datetime.now().strftime(".%m.%Y")
            matricule = rank.firm.acronym + str(
                101 + len(
                    Employee.objects.filter(
                        matricule__contains=fin
                    )
                )
            ) + "N" + fin
            employee.matricule = matricule

        employee.category = category
        employee.rank = rank
        employee.user = user1

        employee._change_reason = json.dumps({
            "reason": "Add a new employee",
            "user": user
        })
        employee._history_date = datetime.now()
        employee.functions.set([function])
        employee.save()
        return employee

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

        self._change_reason = json.dumps({
            "reason": "Update employee",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def delete(self, user: str):
        """ delete employee """
        self.is_active = False

        self._change_reason = json.dumps({
            "reason": "Delete employee",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def restore(self, user: str):
        """ restore employee """
        self.is_active = True

        self._change_reason = json.dumps({
            "reason": "Restore employee",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

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
        url = "/users/" + user + "/"
        conn.request("GET", url, payload, headers)
        response = conn.getresponse()
        dat = response.read()
        data = json.loads(dat)
        return data if data.get('id', 0) != 0 else None

    @staticmethod
    def firms_visibles(user: str, is_superuser=False):
        if is_superuser is True:
            return Firm.objects.all()
        else:
            employees = Employee.objects.filter(is_active=True, user=user)
            firms = []
            for employee in employees:
                if employee.rank.firm.is_active is True:
                    if employee.rank.firm not in firms:
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

    @staticmethod
    def ranks_visibles(user: str, is_superuser=False):
        if is_superuser is True:
            return Rank.objects.all()
        else:
            firms = Employee.firms_visibles(user=user, is_superuser=False)
            ranks = []
            for firm in firms:
                all_firm_rank = firm.ranks.filter(is_active=True)
                for item in all_firm_rank:
                    ranks.append(item)
        return ranks

    @staticmethod
    def employees_visibles(user: str, is_superuser=False):
        if is_superuser is True:
            return Employee.objects.all()
        else:
            employees = []
            ranks = Employee.ranks_visibles(user=user, is_superuser=False)
            for rank in ranks:
                for item in Employee.objects.filter(is_active=True, rank=rank):
                    employees.append(item)
            return employees

    @staticmethod
    def countries_visibles(user: str, is_superuser=False):
        if is_superuser is True:
            return Country.objects.all()
        else:
            functions = Employee.functions_visibles(
                user=user, is_superuser=False)
            portee_max = Portee.objects.filter(
                function__in=functions,
                is_active=True,
                country='ALL'
            )
            if len(portee_max) != 0:
                countries = Country.objects.filter(is_active=True)
            else:
                countries = []
                links = Link.objects.filter(
                    key=1,
                    function__in=functions,
                    is_active=True
                )
                for item in links:
                    country = Country.objects.get(id=item.value)
                    if country not in countries and country.is_active is True:
                        countries.append(country)
            return countries

    @staticmethod
    def regions_visibles(user: str, is_superuser=False):
        if is_superuser is True:
            return Region.objects.all()
        else:
            functions = Employee.functions_visibles(
                user=user, is_superuser=False)
            portee_max = Portee.objects.filter(
                function__in=functions,
                is_active=True,
                region='ALL'
            )
            countries = Employee.countries_visibles(
                user=user, is_superuser=False)
            if len(portee_max) != 0:
                regions = Region.objects.filter(
                    country__in=countries,
                    is_active=True
                )
            else:
                regions = []
                links = Link.objects.filter(
                    key=2,
                    function__in=functions,
                    is_active=True
                )
                for item in links:
                    region = Region.objects.get(id=item.value)
                    if region not in regions and region.is_active is True and region.country in countries:
                        regions.append(region)
            return regions

    @staticmethod
    def departments_visibles(user: str, is_superuser=False):
        if is_superuser is True:
            return Department.objects.all()
        else:
            functions = Employee.functions_visibles(
                user=user, is_superuser=False)
            portee_max = Portee.objects.filter(
                function__in=functions,
                is_active=True,
                department='ALL'
            )
            regions = Employee.regions_visibles(
                user=user, is_superuser=False)
            if len(portee_max) != 0:
                departments = Department.objects.filter(
                    region__in=regions,
                    is_active=True
                )
            else:
                departments = []
                links = Link.objects.filter(
                    key=3,
                    function__in=functions,
                    is_active=True
                )
                for item in links:
                    department = Department.objects.get(id=item.value)
                    if department not in departments and department.is_active is True and department.region in regions:
                        departments.append(department)
            return departments

    @staticmethod
    def municipalities_visibles(user: str, is_superuser=False):
        if is_superuser is True:
            return Municipality.objects.all()
        else:
            functions = Employee.functions_visibles(
                user=user, is_superuser=False)
            portee_max = Portee.objects.filter(
                function__in=functions,
                is_active=True,
                municipality='ALL'
            )
            departments = Employee.departments_visibles(
                user=user, is_superuser=False)
            if len(portee_max) != 0:
                municipalities = Municipality.objects.filter(
                    department__in=departments,
                    is_active=True
                )
            else:
                municipalities = []
                links = Link.objects.filter(
                    key=4,
                    function__in=functions,
                    is_active=True
                )
                for item in links:
                    municipality = Municipality.objects.get(id=item.value)
                    if municipality not in municipalities and municipality.is_active is True and municipality.department in departments:
                        municipalities.append(municipality)
            return municipalities

    @staticmethod
    def villages_visibles(user: str, is_superuser=False):
        if is_superuser is True:
            return Village.objects.all()
        else:
            functions = Employee.functions_visibles(
                user=user, is_superuser=False)
            portee_max = Portee.objects.filter(
                function__in=functions,
                is_active=True,
                village='ALL'
            )
            municipalities = Employee.municipalities_visibles(
                user=user, is_superuser=False)
            if len(portee_max) != 0:
                villages = Village.objects.filter(
                    municipality__in=municipalities,
                    is_active=True
                )
            else:
                villages = []
                links = Link.objects.filter(
                    key=5,
                    function__in=functions,
                    is_active=True
                )
                for item in links:
                    village = Village.objects.get(id=item.value)
                    if village not in villages and village.is_active is True and village.municipality in municipalities:
                        villages.append(village)
            return villages

    @staticmethod
    def sites_visibles(user: str, is_superuser=False):
        if is_superuser is True:
            return Location.objects.all()
        else:
            villages = Employee.villages_visibles(
                user=user, is_superuser=False)
            locations = []
            for item in villages:
                for item1 in item.locations.filter(is_active=True):
                    if item1 not in locations:
                        locations.append(item1)
            return locations
