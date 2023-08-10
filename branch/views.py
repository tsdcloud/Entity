from django.db import DatabaseError
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.http import Http404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from branch.serializers import (
    BranchStoreSerializer, BranchDetailSerializer, BranchDestroySerializer
)

from branch.models import Branch
from firm.models import Firm

from common.permissions import IsDeactivate
from branch.permissions import (
    IsViewAllBranch, IsViewDetailBranch, IsAddBranch, IsChangeBranch,
    IsDestroyBranch, IsRestoreBranch
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
        elif self.action == 'create':
            self.permission_classes = [IsAddBranch]
        elif self.action == 'update':
            self.permission_classes = [IsChangeBranch]
        elif self.action == 'destroy':
            self.permission_classes = [IsDestroyBranch]
        elif self.action == 'restore':
            self.permission_classes = [IsRestoreBranch]
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

    def create(self, request):
        """ add branch """
        serializer = BranchStoreSerializer(data=request.data)
        if serializer.is_valid():
            try:
                firm = Firm.readByToken(
                    token=serializer.validated_data['entity']
                )
                origin = Branch.readByToken(
                    token=serializer.validated_data['start']
                )
                branch = Branch.create(
                    label=serializer.validated_data['label'],
                    firm=firm,
                    origin=origin,
                    is_principal=False,
                    user=request.infoUser.get('uuid')
                )
            except DatabaseError:
                branch = None

            return Response(
                BranchStoreSerializer(branch).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, pk):
        branch = self.get_object()
        serializer = BranchDetailSerializer(
            data=request.data,
            context={"request": request, "branch": branch}
        )
        if serializer.is_valid():
            origin = Branch.readByToken(
                token=serializer.validated_data['start']
            )
            branch.change(
                label=serializer.validated_data['label'],
                origin=origin,
                user=request.infoUser.get('uuid')
            )
            return Response(
                BranchDetailSerializer(
                    branch,
                    context={"request": request, "branch": branch}
                ).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk):
        branch = self.get_object()
        serializer = BranchDestroySerializer(
            data=request.data,
            context={"request": request, "branch": branch}
        )
        if serializer.is_valid():
            branch.delete(
                user=request.infoUser.get('uuid')
            )
            return Response(
                BranchDetailSerializer(
                    branch,
                    context={"request": request, "branch": branch}
                ).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def restore(self, request, pk):
        branch = self.get_object()
        branch.restore(user=request.infoUser.get('uuid'))
        return Response(
                BranchDetailSerializer(
                    branch,
                    context={"request": request, "branch": branch}
                ).data,
                status=status.HTTP_200_OK
            )
