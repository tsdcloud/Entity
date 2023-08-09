import uuid
import os
import datetime

from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _, get_language
from django.template.defaultfilters import slugify

from django.db import models

# Create your models here.
from common.models import BaseUUIDModel
from firm.models import Firm


class Country(models.Model):
    name = models.CharField(_("Country name"), max_length=150)
    iso2 = models.CharField(_("iso2 code"), max_length=2, db_index=True)
    iso3 = models.CharField(_("iso3 code"), max_length=3, db_index=True)
    lang = models.CharField(_("Language"), max_length=15, choices=settings.LANGUAGES, db_index=True)
    is_active = models.BooleanField(_("Is active ?"), default=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            ('name', 'lang'),
            ('iso2', 'lang'),
            ('iso3', 'lang'),
        )
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")


class Region(models.Model):
    name = models.CharField(_("Region"), max_length=150)
    country = models.ForeignKey(Country, db_index=True, on_delete=models.CASCADE)
    lang = models.CharField(_("Language"), max_length=15, choices=settings.LANGUAGES, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            ('name', 'country'),
            ('iso2', 'lang'),
            ('iso3', 'lang'),
        )
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")


class Department(models.Model):
    name = models.CharField(_("Department"), max_length=150)
    region = models.ForeignKey(Region, db_index=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")


class Municipality(models.Model):
    name = models.CharField(_("Municipality"), max_length=150)
    department = models.ForeignKey(Department, db_index=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Municipality")
        verbose_name_plural = _("Municipalities")


class Village(models.Model):
    name = models.CharField(_("Village"), max_length=150)
    department = models.ForeignKey(Municipality, db_index=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Village")
        verbose_name_plural = _("Villages")


class Location(BaseUUIDModel):
    firm = models.ForeignKey(Firm, db_index=True, on_delete=models.CASCADE)
    name = models.CharField(_("Location"), max_length=150, db_index=True)
    village = models.ForeignKey(Village, db_index=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

