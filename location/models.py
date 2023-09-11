from django.utils.translation import ugettext_lazy as _
from django.db import DatabaseError, transaction
from django.db import models
from firm.models import Firm
from function.models import Function
from common.constants import PARTICULAR_PORTEE

# Create your models here.
from common.models import BaseUUIDModel, BaseHistoryModel


class PORTEE(models.Model):
    country = models.IntegerField(choices=PARTICULAR_PORTEE)
    region = models.IntegerField(choices=PARTICULAR_PORTEE)
    departement = models.IntegerField(choices=PARTICULAR_PORTEE)
    municipality = models.IntegerField(choices=PARTICULAR_PORTEE)
    village = models.IntegerField(choices=PARTICULAR_PORTEE)
    function = models.ForeignKey(Function, on_delete=models.RESTRICT)

    def __str__(self):
        return self.function.name

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")


class Link(models.Model):
    key = models.IntegerField(choices=PARTICULAR_PORTEE)
    value = models.CharField(max_length=1000)
    function = models.ForeignKey(Function, on_delete=models.RESTRICT)

    def __str__(self):
        return self.function.name

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")


class Country(BaseUUIDModel):
    name = models.CharField(_("Country name"), max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

    def insertHistory(country: "Country", user: str, operation: int):
        hcountry = HCountry()
        hcountry.country = country
        hcountry.name = country.name
        hcountry.is_active = country.is_active
        hcountry.date = country.date
        hcountry.operation = operation
        hcountry.user = user
        hcountry.save()

    @staticmethod
    def create(name: str, user: str):
        """ add country """
        try:
            country = Country.objects.get(name=name.upper())
        except Country.DoesNotExist:
            country = Country()
            country.name = name.upper()
        country.is_active = True

        try:
            with transaction.atomic():
                country.save()

                Country.insertHistory(country=country, operation=1, user=user)
            return country
        except DatabaseError:
            return None


class HCountry(BaseHistoryModel):
    country = models.ForeignKey(
        Country,
        on_delete=models.RESTRICT,
        related_name="hcontries",
        editable=False
    )
    name = models.CharField(_("Country name"), max_length=150)

    def __str__(self):
        return self.name



class Region(models.Model):
    name = models.CharField(_("Region"), max_length=150)
    country = models.ForeignKey(Country, db_index=True, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")


class Department(models.Model):
    name = models.CharField(_("Department"), max_length=150)
    region = models.ForeignKey(Region, db_index=True, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")


class Municipality(models.Model):
    name = models.CharField(_("Municipality"), max_length=150)
    department = models.ForeignKey(Department, db_index=True, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Municipality")
        verbose_name_plural = _("Municipalities")


class Village(models.Model):
    name = models.CharField(_("Village"), max_length=150)
    department = models.ForeignKey(Municipality, db_index=True, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Village")
        verbose_name_plural = _("Villages")


class Location(BaseUUIDModel):
    firm = models.ForeignKey(Firm, db_index=True, on_delete=models.RESTRICT)
    name = models.CharField(_("Location"), max_length=150, db_index=True)
    village = models.ForeignKey(Village, db_index=True, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name
