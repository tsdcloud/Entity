from django.db import models

# Create your models here.
from function.models import Function
from rank.models import Rank

from user_management.core.models import Member


class Employee(models.Model):
    category = models.CharField(max_length=180)
    rank = models.ForeignKey(Rank, on_delete=models.SET_NULL)
    function = models.ForeignKey(Function, on_delete=models.SET_NULL)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.category, self.member.full_name)

