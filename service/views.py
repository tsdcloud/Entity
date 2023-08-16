from django.db import DatabaseError
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.http import Http404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from service.serializers import (
    ServiceStoreSerializer, ServiceDetailSerializer,
    ServiceDestroySerializer, ServiceRestoreSerializer
)

from branch.models import Branch
from service.models import Service

from common.permissions import IsDeactivate
from service.permissions import (
    IsAddService, IsChangeService, IsDestroyService, IsRestoreService,
    IsViewAllService, IsViewDetailService
)


class ServiceViewSet(viewsets.ModelViewSet):
    """ service controller """

    def get_serializer_class(self):
        """ define serializer """
        if self.action in ['retrieve', 'update']:
            return ServiceDetailSerializer
        return ServiceStoreSerializer

    def get_permissions(self):
        """ define permissions """
        if self.action == 'list':
            self.permission_classes = [IsViewAllService]
        elif self.action == 'retrieve':
            self.permission_classes = [IsViewDetailService]
        elif self.action == 'create':
            self.permission_classes = [IsAddService]
        elif self.action == 'update':
            self.permission_classes = [IsChangeService]
        elif self.action == 'destroy':
            self.permission_classes = [IsDestroyService]
        elif self.action == 'restore':
            self.permission_classes = [IsRestoreService]
        else:
            self.permission_classes = [IsDeactivate]
        return super().get_permissions()

    def get_queryset(self):
        """ define queryset """
        if self.request.infoUser['user']['is_superuser'] is True:
            queryset = Service.objects.all()
        else:
            queryset = Service.objects.filter(is_active=True)
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
        """ add service """
        serializer = ServiceStoreSerializer(data=request.data)
        if serializer.is_valid():
            try:
                branch = Branch.readByToken(
                    token=serializer.validated_data['branch_id']
                )
                service = Service.create(
                    name=serializer.validated_data['name'],
                    description=serializer.validated_data['description'],
                    branch=branch,
                    user=request.infoUser.get('uuid')
                )
            except DatabaseError:
                service = None

            return Response(
                ServiceStoreSerializer(service).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, pk):
        service = self.get_object()
        serializer = ServiceDetailSerializer(
            data=request.data,
            context={"request": request, "service": service}
        )
        if serializer.is_valid():
            branch = Branch.readByToken(
                token=serializer.validated_data['branch_id']
            )
            service.change(
                name=serializer.validated_data['name'],
                description=serializer.validated_data['description'],
                branch=branch,
                user=request.infoUser.get('uuid')
            )
            return Response(
                ServiceDetailSerializer(
                    service,
                    context={"request": request, "service": service}
                ).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk):
        service = self.get_object()
        serializer = ServiceDestroySerializer(
            data=request.data,
            context={"request": request, "service": service}
        )
        if serializer.is_valid():
            service.delete(
                user=request.infoUser.get('uuid')
            )
            return Response(
                ServiceDetailSerializer(
                    service,
                    context={"request": request, "service": service}
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
        service = self.get_object()
        serializer = ServiceRestoreSerializer(
            data=request.data,
            context={"request": request, "service": service}
        )
        if serializer.is_valid():
            service.restore(user=request.infoUser.get('uuid'))
            return Response(
                    ServiceDetailSerializer(
                        service,
                        context={"request": request, "service": service}
                    ).data,
                    status=status.HTTP_200_OK
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
