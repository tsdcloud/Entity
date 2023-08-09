from django.shortcuts import get_object_or_404
from django.db import DatabaseError, transaction

from rest_framework import viewsets, status
from rest_framework.response import Response

from firm.serializers import FirmStoreSerializer

from firm.models import Firm
from branch.models import Branch

from common.permissions import IsDeactivate
from . permissions import IsAddFirm


class FirmViewSet(viewsets.ModelViewSet):
    """ firm controller """

    def get_serializer_class(self):
        """ define serializer """
        return FirmStoreSerializer

    def get_permissions(self):
        """ define permissions """
        if self.action == 'create':
            self.permission_classes = [IsAddFirm]
        else:
            self.permission_classes = [IsDeactivate]
        return super().get_permissions()

    def get_queryset(self):
        """ define queryset """
        if self.request.infoUser.get('is_superuser'):
            queryset = Firm.objects.all()
        else:
            queryset = Firm.objects.filter(active=True)
        return queryset

    def get_object(self):
        """ define object on detail url """
        if self.request.infoUser.get('is_superuser'):
            r = Firm.objects.filter(uuid=self.kwargs['pk'])
        else:
            r = Firm.objects.filter(uuid=self.kwargs['pk'], active=True)
        obj = get_object_or_404(r, uuid=self.kwargs["pk"])
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
