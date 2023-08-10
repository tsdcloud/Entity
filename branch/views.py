from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.http import Http404

from rest_framework import viewsets

from branch.serializers import (
    BranchStoreSerializer, BranchDetailSerializer
)

from branch.models import Branch

from common.permissions import IsDeactivate
from branch.permissions import (
    IsViewAllBranch, IsViewDetailBranch
)


class BranchViewSet(viewsets.ModelViewSet):
    """ branch controller """

    def get_serializer_class(self):
        """ define serializer """
        if self.action in ['retrieve', 'update']:
            return BranchDetailSerializer
        return BranchStoreSerializer

    def get_permissions(self):
        """ define permissions """
        if self.action == 'list':
            self.permission_classes = [IsViewAllBranch]
        elif self.action == 'retrieve':
            self.permission_classes = [IsViewDetailBranch]
        else:
            self.permission_classes = [IsDeactivate]
        return super().get_permissions()

    def get_queryset(self):
        """ define queryset """
        if self.request.infoUser.get('is_superuser'):
            queryset = Branch.objects.all()
        else:
            queryset = Branch.objects.filter(is_active=True)
        return queryset

    def get_object(self):
        """ define object on detail url """
        try:
            if self.request.infoUser.get('is_superuser'):
                r = Branch.objects.filter(id=self.kwargs['pk'])
            else:
                r = Branch.objects.filter(id=self.kwargs['pk'], is_active=True)
            obj = get_object_or_404(r, id=self.kwargs["pk"])
        except ValidationError:
            raise Http404("detail not found")
        return obj
