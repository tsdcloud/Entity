from django.shortcuts import get_object_or_404
from django.db import DatabaseError, transaction

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from firm.serializers import FirmStoreSerializer, FirmDetailSerializer

from firm.models import Firm
from branch.models import Branch

from common.permissions import IsDeactivate
from . permissions import IsAddFirm, IsViewAllFirm, IsViewDetailFirm, IsChangeFirm

class FirmViewSet(viewsets.ModelViewSet):
    """ firm controller """

    def get_serializer_class(self):
        """ define serializer """
        if self.action in ['retrieve','update']:
            return FirmDetailSerializer
        return FirmStoreSerializer
        #return super().get_serializer_class()

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
        #elif self.action == 'destroy':
         #   self.permission_classes = [IsDeactivate]
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
            r=Firm.objects.filter(uuid=self.kwargs['pk'])
        else:
            r=Firm.objects.filter(uuid=self.kwargs['pk'],active=True)
        obj = get_object_or_404(r, uuid=self.kwargs["pk"])
        return obj

    def create(self, request):
        """ add entity """
        serializer = FirmStoreSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    firm = Firm.create(
                        social_raison=serializer.validated_data['social_raison'],
                        sigle=serializer.validated_data['sigle'],
                        niu=serializer.validated_data['niu'],
                        principal_activity=serializer.validated_data['principal_activity'],
                        regime = serializer.validated_data['regime'],
                        tax_reporting_center=serializer.validated_data['tax_reporting_center'],
                        trade_register=serializer.validated_data['trade_register'],
                        logo = serializer.validated_data['logo'],
                        type_person=serializer.validated_data['type_person'],
                        user = request.infoUser.get('uuid')
                    )
                    Branch.create(libelle="principale", firm=firm, origine="START", principal=True, user=request.infoUser.get('uuid'))
            except DatabaseError:
                firm = None
            
            return Response(FirmStoreSerializer(firm).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request,pk):
        firm = self.get_object()
        serializer = FirmDetailSerializer(data=request.data, context={"request":request, "firm":firm})
        if serializer.is_valid():
            firm.change(
                social_raison=serializer.validated_data['social_raison'],
                sigle=serializer.validated_data['sigle'],
                niu=serializer.validated_data['niu'],
                principal_activity=serializer.validated_data['principal_activity'],
                regime=serializer.validated_data['regime'],
                tax_reporting_center=serializer.validated_data['tax_reporting_center'],
                trade_register=serializer.validated_data['trade_register'],
                logo=serializer.validated_data['logo'],
                type_person=serializer.validated_data['type_person'],
                user=request.infoUser.get('uuid')
            )
            return Response(FirmDetailSerializer(firm,context={"request":request, "firm":firm}).data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)