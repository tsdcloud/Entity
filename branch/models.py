from django.db import models
from django.db import DatabaseError, transaction


from common.models import BaseUUIDModel
from common.constants import H_OPERATION_CHOICE

from firm.models import Firm


class Branch(BaseUUIDModel):
    firm = models.ForeignKey(
        Firm, on_delete=models.RESTRICT, related_name="branchs")
    label = models.CharField(unique=True, max_length=100)
    origin = models.ForeignKey(
        "Branch",
        on_delete=models.RESTRICT, null=True)
    is_principal = models.BooleanField(default=False)
    is_service = models.BooleanField(default=False)

    def __str__(self):
        return self.label

    class Meta:
        """ defined how the data will be shouted into the database """
        ordering = ["is_principal", "label", "date"]

    @staticmethod
    def create(
        label: str,
        firm: Firm,
        origin: "Branch",
        is_principal: bool,
        user: str
    ):
        """ add branch """
        branch = Branch()
        branch.label = label.upper()
        branch.firm = firm
        if is_principal is False:
            branch.origin = origin
        branch.is_principal = is_principal

        h_branch = HBranch()

        try:
            with transaction.atomic():
                branch.save()

                h_branch.branch = branch
                h_branch.label = branch.label
                h_branch.firm = branch.firm
                h_branch.origin = branch.origin
                h_branch.is_principal = branch.is_principal
                h_branch.is_active = branch.is_active
                h_branch.date = branch.date
                h_branch.operation = 1
                h_branch.user = user

                h_branch.save()

            return branch
        except DatabaseError:
            return None

    @classmethod
    def readByToken(cls, token: str):
        return cls.objects.get(id=token)

    def change(self, label: str, origin: "Branch", user: str):
        """ update branch"""
        self.label = label.upper()
        self.origin = origin
        self.user = user

        h_branch = HBranch()

        try:
            with transaction.atomic():
                self.save()

                h_branch.branch = self
                h_branch.label = self.label
                h_branch.firm = self.firm
                h_branch.origin = self.origin
                h_branch.is_principal = self.is_principal
                h_branch.is_active = self.is_active
                h_branch.date = self.date
                h_branch.operation = 2
                h_branch.user = user

                h_branch.save()

            return self
        except DatabaseError:
            return None

    def delete(self, user: str):
        self.is_active = False

        h_branch = HBranch()

        try:
            with transaction.atomic():
                self.save()

                h_branch.branch = self
                h_branch.label = self.label
                h_branch.firm = self.firm
                h_branch.origin = self.origin
                h_branch.is_principal = self.is_principal
                h_branch.is_active = self.is_active
                h_branch.date = self.date
                h_branch.operation = 3
                h_branch.user = user

                h_branch.save()

            return self
        except DatabaseError:
            return None

    def restore(self, user: str):
        self.is_active = True

        h_branch = HBranch()

        try:
            with transaction.atomic():
                self.save()

                h_branch.branch = self
                h_branch.label = self.label
                h_branch.firm = self.firm
                h_branch.origin = self.origin
                h_branch.is_principal = self.is_principal
                h_branch.is_active = self.is_active
                h_branch.date = self.date
                h_branch.operation = 4
                h_branch.user = user

                h_branch.save()

            return self
        except DatabaseError:
            return None


class HBranch(models.Model):
    """ branch update history """
    branch = models.ForeignKey(
        Branch,
        on_delete=models.RESTRICT, related_name="hbranchs", editable=False)
    label = models.CharField(
        verbose_name="Label",
        max_length=100, editable=False)
    firm = models.ForeignKey(
        Firm,
        on_delete=models.RESTRICT, related_name="hbranchs", editable=False)
    origin = models.ForeignKey(
        Branch,
        on_delete=models.RESTRICT,
        related_name="hbranchs_origins", null=True, editable=False)
    is_principal = models.BooleanField(default=False)
    is_service = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, editable=False)
    date = models.DateTimeField(editable=False)
    operation = models.IntegerField(choices=H_OPERATION_CHOICE, editable=False)
    user = models.CharField(editable=False, max_length=1000)
    dateop = models.DateTimeField(auto_now_add=True, editable=False)
