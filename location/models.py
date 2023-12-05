from django.utils.translation import ugettext_lazy as _
from simple_history.models import HistoricalRecords
from django.db import models
from firm.models import Firm
from function.models import Function
from common.constants import PARTICULAR_PORTEE, PARTICULAR_PORTEE_KEY
import json
from datetime import datetime

# Create your models here.
from common.models import BaseUUIDModel


class Portee(BaseUUIDModel):
    country = models.IntegerField(choices=PARTICULAR_PORTEE)
    region = models.IntegerField(choices=PARTICULAR_PORTEE)
    departement = models.IntegerField(choices=PARTICULAR_PORTEE)
    municipality = models.IntegerField(choices=PARTICULAR_PORTEE)
    village = models.IntegerField(choices=PARTICULAR_PORTEE)
    function = models.ForeignKey(Function, on_delete=models.RESTRICT)
    history = HistoricalRecords()

    def __str__(self):
        return self.function.name

    class Meta:
        ordering = []


class Link(BaseUUIDModel):
    key = models.IntegerField(choices=PARTICULAR_PORTEE_KEY)
    value = models.CharField(max_length=1000)
    function = models.ForeignKey(Function, on_delete=models.RESTRICT)
    history = HistoricalRecords()

    def __str__(self):
        return self.function.name

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")


class Country(BaseUUIDModel):
    name = models.CharField(_("Country name"), max_length=150)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

    @staticmethod
    def create(name: str, user: str):
        """ add country """
        try:
            country = Country.objects.get(name=name.upper())
        except Country.DoesNotExist:
            country = Country()
            country.name = name.upper()
        country.is_active = True

        country._change_reason = json.dumps({
            "reason": "Add a new country",
            "user": user
        })
        country._history_date = datetime.now()
        country.save()
        return country

    def change(self, name: str, user: str):
        """ update country """
        self.name = name.upper()

        self._change_reason = json.dumps({
            "reason": "Update country",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def delete(self, user: str):
        """ delete country """
        self.is_active = False

        self._change_reason = json.dumps({
            "reason": "Delete a country",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def restore(self, user: str):
        """ restore country """
        self.is_active = True
        self._change_reason = json.dumps({
            "reason": "Restore a country",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self


class Region(BaseUUIDModel):
    name = models.CharField(_("Region"), max_length=150)
    country = models.ForeignKey(
        Country,
        db_index=True,
        on_delete=models.RESTRICT,
        related_name="regions"
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")

    def create(country: Country, name: str, user: str):
        """ add region """
        try:
            region = Region.objects.get(country=country, name=name.upper())
        except Region.DoesNotExist:
            region = Region()
            region.name = name.upper()
            region.country = country
        region.is_active = True

        region._change_reason = json.dumps({
            "reason": "Add a new region",
            "user": user
        })
        region._history_date = datetime.now()
        region.save()
        return region

    def change(self, name: str, user: str):
        """ update region """
        self.name = name.upper()

        self._change_reason = json.dumps({
            "reason": "Update region",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def delete(self, user: str):
        """ delete region """
        self.is_active = False

        self._change_reason = json.dumps({
            "reason": "Delete a region",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def restore(self, user: str):
        """ restore region """
        self.is_active = True

        self._change_reason = json.dumps({
            "reason": "Restore a region",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self


class Department(BaseUUIDModel):
    name = models.CharField(_("Department"), max_length=150)
    region = models.ForeignKey(
        Region,
        db_index=True,
        on_delete=models.RESTRICT,
        related_name="departments"
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")

    def create(region: Region, name: str, user: str):
        """ add department """
        try:
            department = Department.objects.get(
                region=region, name=name.upper()
            )
        except Department.DoesNotExist:
            department = Department()
            department.name = name.upper()
            department.region = region
        department.is_active = True

        department._change_reason = json.dumps({
            "reason": "Add a new department",
            "user": user
        })
        department._history_date = datetime.now()
        department.save()
        return department

    def change(self, name: str, user: str):
        """ update department """
        self.name = name.upper()

        self._change_reason = json.dumps({
            "reason": "Change a department",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def delete(self, user: str):
        """ delete department """
        self.is_active = False

        self._change_reason = json.dumps({
            "reason": "Delete a department",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def restore(self, user: str):
        """ restore department """
        self.is_active = True

        self._change_reason = json.dumps({
            "reason": "Restore a department",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self


class Municipality(BaseUUIDModel):
    name = models.CharField(_("Municipality"), max_length=150)
    department = models.ForeignKey(
        Department,
        db_index=True,
        on_delete=models.RESTRICT,
        related_name="municipalities"
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Municipality")
        verbose_name_plural = _("Municipalities")

    @staticmethod
    def create(department: Department, name: str, user: str):
        """ add municipality """
        try:
            municipality = Municipality.objects.get(
                department=department, name=name.upper()
            )
        except Municipality.DoesNotExist:
            municipality = Municipality()
            municipality.name = name.upper()
            municipality.department = department
        municipality.is_active = True

        municipality._change_reason = json.dumps({
            "reason": "Add a new municipality",
            "user": user
        })
        municipality._history_date = datetime.now()
        municipality.save()
        return municipality

    def change(self, name: str, user: str):
        """ update municipality """
        self.name = name.upper()

        self._change_reason = json.dumps({
            "reason": "Update a municipality",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def delete(self, user: str):
        """ delete municipality """
        self.is_active = False

        self._change_reason = json.dumps({
            "reason": "Delete a municipality",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def restore(self, user: str):
        """ restore municipality """
        self.is_active = True

        self._change_reason = json.dumps({
            "reason": "Restore a municipality",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self


class Village(BaseUUIDModel):
    name = models.CharField(_("Village"), max_length=150)
    municipality = models.ForeignKey(
        Municipality,
        db_index=True,
        on_delete=models.RESTRICT,
        related_name="villages"
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Village")
        verbose_name_plural = _("Villages")

    @staticmethod
    def create(municipality: Municipality, name: str, user: str):
        """ add village """
        try:
            village = Village.objects.get(
                municipality=municipality, name=name.upper()
            )
        except Village.DoesNotExist:
            village = Village()
            village.name = name.upper()
            village.municipality = municipality
        village.is_active = True

        village._change_reason = json.dumps({
            "reason": "Add a new village",
            "user": user
        })
        village._history_date = datetime.now()
        village.save()
        return village

    def change(self, name: str, user: str):
        """ update village """
        self.name = name.upper()

        self._change_reason = json.dumps({
            "reason": "Update a village",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def delete(self, user: str):
        """ delete village """
        self.is_active = False

        self._change_reason = json.dumps({
            "reason": "Add a new country",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def restore(self, user: str):
        """ restore village """
        self.is_active = True

        self._change_reason = json.dumps({
            "reason": "Restore a village",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self


class Location(BaseUUIDModel):
    firm = models.ForeignKey(
        Firm,
        db_index=True,
        on_delete=models.RESTRICT,
        related_name="locations"
    )
    name = models.CharField(_("Location"), max_length=150, db_index=True)
    village = models.ForeignKey(
        Village,
        db_index=True,
        on_delete=models.RESTRICT,
        related_name="locations"
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    @staticmethod
    def create(firm: Firm, village: Village, name: str, user: str):
        """ add location """
        try:
            location = Location.objects.get(
                firm=firm,
                village=village,
                name=name.upper()
            )
        except Location.DoesNotExist:
            location = Location()
            location.name = name.upper()
            location.firm = firm
            location.village = village
        location.is_active = True

        location._change_reason = json.dumps({
            "reason": "Add a new location",
            "user": user
        })
        location._history_date = datetime.now()
        location.save()
        return location

    def change(self, name: str, user: str):
        """ update location """
        self.name = name.upper()

        self._change_reason = json.dumps({
            "reason": "Update a location",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def delete(self, user: str):
        """ delete location """
        self.is_active = False

        self._change_reason = json.dumps({
            "reason": "Delete a location",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self

    def restore(self, user: str):
        """ restore location """
        self.is_active = True

        self._change_reason = json.dumps({
            "reason": "Restore a country",
            "user": user
        })
        self._history_date = datetime.now()
        self.save()
        return self
