from django.db import models
from django.db import DatabaseError, transaction


from common.models import BaseUUIDModel
from common.constants import H_OPERATION_CHOICE

from firm.models import Firm


class Branch(BaseUUIDModel):
    firm = models.ForeignKey(Firm, on_delete=models.RESTRICT, related_name="branches")
    label = models.CharField(unique=True)
    origin = models.ForeignKey("Branch", on_delete=models.RESTRICT, related_name="branches", null=True)
    is_principal = models.BooleanField(default=False)

    def __str__(self):
        return self.label

    class Meta:
        """ defined how the data will be shouted into the database """
        ordering = ["is_principal", "label", "date"]

    @staticmethod
    def create(label: str, firm: Firm, origin: str, principal: bool, user: str):
        """ add branch """
        branch = Branch()
        branch.label = label.upper()
        branch.firm = firm
        branch.origin = origin
        branch.principal = principal

        h_branch = HBranch()

        try:
            with transaction.atomic():
                branch.save()

                branch.id += ':' + str(branch.pk)

                branch.save()

                h_branch.branch = branch
                h_branch.id = branch.id
                h_branch.label = branch.label
                h_branch.firm = branch.firm
                h_branch.origin = branch.origin
                h_branch.principal = branch.principal
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
        return cls.objects.get(uuid=token)


class HBranch(BaseUUIDModel):
    """ historiques des mise a jour des branches """
    branch = models.ForeignKey(Branch, on_delete=models.RESTRICT, related_name="h_branchs", editable=False)
    label = models.CharField(_("Label"), max_length=10, editable=False)
    firm = models.ForeignKey(Firm, on_delete=models.RESTRICT, related_name="h_branchs", editable=False)
    principal = models.BooleanField(default=True, editable=False)
    operation = models.IntegerField(choices=H_OPERATION_CHOICE, editable=False)
    user = models.CharField(editable=False, max_length=1000)
    dateop = models.DateTimeField(auto_now_add=True, editable=False)