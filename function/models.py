from django.db import models

# Create your models here.
from service.models import Service


class Function(models.Model):
    name = models.CharField(max_length=180)
    power = models.IntegerField()
    description = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

