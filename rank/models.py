from django.db import models

# Create your models here.
from firm.models import Firm


class Rank(models.Model):
    label = models.CharField(max_length=150)
    power = models.IntegerField()
    entity = models.ForeignKey(Firm, on_delete=models.CASCADE)

    def __str__(self):
        return self.label

