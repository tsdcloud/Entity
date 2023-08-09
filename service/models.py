from django.db import models

# Create your models here.

from branch.models import *


class Service(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    active = models.BooleanField(default=False)
    date = models.DateTimeField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.name
