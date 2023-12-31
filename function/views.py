from django.db import DatabaseError
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.http import Http404
from django.contrib.auth.models import Permission

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from function.serializers import (
    FunctionStoreSerializer, FunctionDetailSerializer,
    FunctionDestroySerializer, FunctionRestoreSerializer,
    FunctionAddPermissionSerializer
)

from function.models import Function
from service.models import Service
from employee.models import Employee

from common.permissions import IsDeactivate, IsAddPermission
from function.permissions import (
    IsAddFunction, IsChangeFunction, IsDestroyFunction,
    IsRestoreFunction, IsViewAllFunction, IsViewDetailFunction
)


class FunctionViewSet(viewsets.ModelViewSet):
    """ function controller """

    def get_serializer_class(self):
        """ define serializer """
        if self.action in ['retrieve', 'update']:
            return FunctionDetailSerializer
        elif self.action == 'destroy':
            return FunctionDestroySerializer
        elif self.action == 'restore':
            return FunctionRestoreSerializer
        return FunctionStoreSerializer

    def get_permissions(self):
        """ define permissions """
        if self.action == 'list':
            self.permission_classes = [IsViewAllFunction]
        elif self.action == 'retrieve':
            self.permission_classes = [IsViewDetailFunction]
        elif self.action == 'create':
            self.permission_classes = [IsAddFunction]
        elif self.action == 'update':
            self.permission_classes = [IsChangeFunction]
        elif self.action == 'destroy':
            self.permission_classes = [IsDestroyFunction]
        elif self.action == 'restore':
            self.permission_classes = [IsRestoreFunction]
        elif self.action == 'permissions':
            self.permission_classes = [IsAddPermission]
        else:
            self.permission_classes = [IsDeactivate]
        return super().get_permissions()

    def get_queryset(self):
        """ define queryset """
        queryset = Employee.functions_visibles(
            user=self.request.infoUser['id'],
            is_superuser=self.request.infoUser['member']['is_superuser']
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
        """ add function """
        serializer = FunctionStoreSerializer(
            data=request.data,
            context={"request": request, "queryset": self.get_queryset()}
        )
        if serializer.is_valid():
            try:
                service = Service.readByToken(
                    token=serializer.validated_data['service_id'])
                function = Function.create(
                    name=serializer.validated_data['name'],
                    power=serializer.validated_data['power'],
                    description=serializer.validated_data['description'],
                    service=service,
                    user=request.infoUser.get('id')
                )
            except DatabaseError:
                function = None

            return Response(
                FunctionStoreSerializer(
                    function,
                    context={
                        "request": request,
                        "queryset": self.get_queryset()
                    }
                ).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, pk):
        function = self.get_object()
        serializer = FunctionDetailSerializer(
            data=request.data,
            context={"request": request, "function": function}
        )
        if serializer.is_valid():
            service = Service.readByToken(
                token=serializer.validated_data['service_id'])
            function.change(
                name=serializer.validated_data['name'],
                power=serializer.validated_data['power'],
                description=serializer.validated_data['description'],
                service=service,
                user=request.infoUser.get('id')
            )
            return Response(
                FunctionDetailSerializer(
                    function,
                    context={"request": request, "function": function}
                ).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk):
        function = self.get_object()
        serializer = FunctionDestroySerializer(
            function,
            context={"request": request, "function": function}
        )
        if serializer.is_valid():
            function.delete(
                user=request.infoUser.get('id')
            )
            return Response(
                FunctionDetailSerializer(
                    function,
                    context={"request": request, "function": function}
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
        function = self.get_object()
        serializer = FunctionRestoreSerializer(
            data=request.data,
            context={"request": request, "function": function}
        )
        if serializer.is_valid():
            function.restore(user=request.infoUser.get('id'))
            return Response(
                    FunctionDetailSerializer(
                        function,
                        context={"request": request, "function": function}
                    ).data,
                    status=status.HTTP_200_OK
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def permissions(self, request, pk):
        function = self.get_object()
        serializer = FunctionAddPermissionSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            permissions = []
            for codename in serializer.validated_data['permissions']:
                permissions.append(
                    Permission.objects.get(codename=codename)
                )
            function.add_permission(
                user=request.infoUser.get('id'),
                permissions=permissions
            )
            return Response(
                FunctionDetailSerializer(
                    function,
                    context={"request": request, "function": function}
                ).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
