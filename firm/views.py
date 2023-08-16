from django.shortcuts import get_object_or_404
from django.db import DatabaseError, transaction
from django.core.exceptions import ValidationError
from django.http import Http404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from firm.serializers import FirmStoreSerializer, FirmDetailSerializer
from branch.serializers import BranchStoreSerializer

from firm.models import Firm
from branch.models import Branch
from employee.models import Employee

from common.permissions import IsDeactivate
from . permissions import (
    IsAddFirm, IsChangeFirm, IsDestroyFirm, IsRestoreFirm,
    IsViewAllFirm, IsViewDetailFirm
)
from branch.permissions import IsViewAllBranch


class FirmViewSet(viewsets.ModelViewSet):
    """ firm controller """

    def get_serializer_class(self):
        """ define serializer """
        if self.action in ['retrieve', 'update']:
            return FirmDetailSerializer
        return FirmStoreSerializer

    def get_permissions(self):
        """ define permissions """
        if self.action == 'create':
            self.permission_classes = [IsAddFirm]
        elif self.action == 'list':
            self.permission_classes = [IsViewAllFirm]
        elif self.action == 'retrieve':
            self.permission_classes = [IsViewDetailFirm]
        elif self.action == 'update':
            self.permission_classes = [IsChangeFirm]
        elif self.action == 'destroy':
            self.permission_classes = [IsDestroyFirm]
        elif self.action == 'restore':
            self.permission_classes = [IsRestoreFirm]
        elif self.action == 'branchs':
            self.permission_classes = [IsViewAllBranch]
        else:
            self.permission_classes = [IsDeactivate]
        return super().get_permissions()

    def get_queryset(self):
        """ define queryset """
        if self.request.infoUser['user']['is_superuser'] is True:
            queryset = Firm.objects.all()
        else:
            queryset = Employee.firms_visibles(
                user=self.request.infoUser.get('uuid')
            )
        return queryset

    def get_object(self):
        """ define object on detail url """
        queryset = self.get_queryset()
        try:
            obj = get_object_or_404(queryset, id=self.kwargs["pk"])
        except ValidationError:
            raise Http404("detail not found")
        return obj

    def create(self, request):
        """ add entity """
        serializer = FirmStoreSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    firm = Firm.create(
                        acronym=serializer.validated_data['acronym'],
                        business_name=serializer.validated_data[
                            'business_name'],
                        logo=serializer.validated_data['logo'],
                        principal_activity=serializer.validated_data[
                            'principal_activity'],
                        regime=serializer.validated_data['regime'],
                        tax_reporting_center=serializer.validated_data[
                            'tax_reporting_center'],
                        trade_register=serializer.validated_data[
                            'trade_register'],
                        type_person=serializer.validated_data['type_person'],
                        unique_identifier_number=serializer.validated_data[
                            'unique_identifier_number'],
                        user=request.infoUser.get('uuid')
                    )
                    Branch.create(
                        label="principale",
                        firm=firm,
                        origin=Branch(),
                        is_principal=True,
                        user=request.infoUser.get('uuid')
                    )
            except DatabaseError:
                firm = None

            return Response(
                FirmStoreSerializer(firm).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, pk):
        firm = self.get_object()
        serializer = FirmDetailSerializer(
            data=request.data,
            context={"request": request, "firm": firm}
        )
        if serializer.is_valid():
            firm.change(
                acronym=serializer.validated_data['acronym'],
                business_name=serializer.validated_data['business_name'],
                unique_identifier_number=serializer.validated_data[
                    'unique_identifier_number'
                ],
                principal_activity=serializer.validated_data[
                    'principal_activity'
                ],
                regime=serializer.validated_data['regime'],
                tax_reporting_center=serializer.validated_data[
                    'tax_reporting_center'
                ],
                trade_register=serializer.validated_data['trade_register'],
                logo=serializer.validated_data['logo'],
                type_person=serializer.validated_data['type_person'],
                user=request.infoUser.get('uuid')
            )
            return Response(
                FirmDetailSerializer(
                    firm,
                    context={"request": request, "firm": firm}
                ).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk):
        firm = self.get_object()
        firm.delete(user=self.request.infoUser.get('uuid'))
        return Response(
                FirmDetailSerializer(
                    firm,
                    context={"request": request, "firm": firm}
                ).data,
                status=status.HTTP_200_OK
            )

    @action(detail=True, methods=['post'])
    def restore(self, request, pk):
        """ restore an entity """
        firm = self.get_object()
        firm.restore(user=request.infoUser.get('uuid'))
        return Response(
                FirmDetailSerializer(
                    firm,
                    context={"request": request, "firm": firm}
                ).data,
                status=status.HTTP_200_OK
            )

    @action(detail=True, methods=['get'])
    def branchs(self, request, pk):
        """ listing of branch's firm """
        firm = self.get_object()
        branchs = Branch.objects.filter(
            firm=firm,
            is_active=self.request.infoUser['user']['is_superuser']
        )
        queryset = self.filter_queryset(branchs)
        page = self.paginate_queryset(queryset=queryset)
        if page is not None:
            serializer = BranchStoreSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(
                BranchStoreSerializer(
                    branchs,
                    context={"request": request},
                    many=True
                ).data,
                status=status.HTTP_200_OK
            )
