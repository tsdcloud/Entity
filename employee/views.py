from django.db import DatabaseError
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.http import Http404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from employee.serializers import (
    EmployeeStoreSerializer, EmployeeDetailSerializer
)

from employee.models import Employee
from rank.models import Rank
from function.models import Function

from common.permissions import IsDeactivate
from employee.permissions import (
    IsAddEmployee, IsChangeEmployee, IsDestroyEmployee,
    IsRestoreEmployee, IsViewAllEmployee, IsViewDetailEmployee
)


class EmployeeViewSet(viewsets.ModelViewSet):
    """ Employee controller """

    def get_serializer_class(self):
        """ define serializer """
        if self.action in ['retrieve', 'update']:
            return EmployeeDetailSerializer
        return EmployeeStoreSerializer

    def get_permissions(self):
        """ define permissions """
        if self.action == 'list':
            self.permission_classes = [IsViewAllEmployee]
        elif self.action == 'retrieve':
            self.permission_classes = [IsViewDetailEmployee]
        elif self.action == 'create':
            self.permission_classes = [IsAddEmployee]
        elif self.action == 'update':
            self.permission_classes = [IsChangeEmployee]
        elif self.action == 'destroy':
            self.permission_classes = [IsDestroyEmployee]
        elif self.action == 'restore':
            self.permission_classes = [IsRestoreEmployee]
        else:
            self.permission_classes = [IsDeactivate]
        return super().get_permissions()

    def get_queryset(self):
        """ define queryset """
        if self.request.infoUser['user']['is_superuser'] is True:
            queryset = Employee.objects.all()
        else:
            queryset = Employee.employees_visibles(
                user=self.request.infoUser.get('uuid'),
                is_superuser=False
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
        """ add employee """
        serializer = EmployeeStoreSerializer(
            data=request.data,
            context={
                "request": request
            }
        )
        if serializer.is_valid():
            try:
                rank = Rank.readByToken(
                    token=serializer.validated_data['rank_id']
                )
                function = Function.readByToken(
                    token=serializer.validated_data['function_id']
                )
                employee = Employee.create(
                    user1=serializer.validated_data['user_id'],
                    category=serializer.validated_data['category'],
                    rank=rank,
                    function=function,
                    user=request.infoUser.get('uuid')
                )
            except DatabaseError:
                employee = None

            return Response(
                EmployeeStoreSerializer(
                    employee,
                    context={
                        "request": request
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
        employee = self.get_object()
        serializer = EmployeeDetailSerializer(
            data=request.data,
            context={"request": request, "employee": employee}
        )
        if serializer.is_valid():
            rank = Rank.readByToken(
                token=serializer.validated_data['rank_id']
            )
            function = Function.readByToken(
                token=serializer.validated_data['function_id']
            )
            employee.change(
                category=serializer.validated_data['category'],
                rank=rank,
                function=function,
                user=request.infoUser.get('uuid')
            )
            return Response(
                EmployeeDetailSerializer(
                    employee,
                    context={"request": request, "employee": employee}
                ).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk):
        employee = self.get_object()
        employee.delete(user=request.infoUser.get('uuid'))
        return Response(
            EmployeeDetailSerializer(
                employee,
                context={"request": request, "employee": employee}
            ).data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def restore(self, request, pk):
        employee = self.get_object()
        employee.restore(user=request.infoUser.get('uuid'))
        return Response(
            EmployeeDetailSerializer(
                employee,
                context={"request": request, "employee": employee}
            ).data,
            status=status.HTTP_200_OK
        )
