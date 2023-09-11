from django.db import DatabaseError
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.http import Http404
from django.contrib.auth.models import Permission

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from function.serializers import (
    FunctionDetailSerializer,
    FunctionDestroySerializer, FunctionRestoreSerializer,
    FunctionAddPermissionSerializer
)

from service.models import Service

from common.permissions import IsDeactivate, IsActivate

from location.serializers import (
    CountryStoreSerializer,
    CountryDetailSerializer
)
from location.permissions import (
    IsAddLocation
)
from location.models import (
    Country
)


class CountryViewSet(viewsets.ModelViewSet):
    """ country controller """

    def get_serializer_class(self):
        """ define serializer """
        if self.action in ['retrieve', 'update']:
            return CountryDetailSerializer
        elif self.action == 'destroy':
            return FunctionDestroySerializer
        elif self.action == 'restore':
            return FunctionRestoreSerializer
        return CountryStoreSerializer

    def get_permissions(self):
        """ define permissions """
        if self.action in ["create", "update"]:
            self.permission_classes = [IsAddLocation]
        elif self.action == 'list':
            self.permission_classes = [IsActivate]
        else:
            self.permission_classes = [IsDeactivate]
        return super().get_permissions()

    def get_queryset(self):
        """ define queryset """
        queryset = Country.objects.filter(is_active=True)
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
        """ add country """
        serializer = CountryStoreSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            try:
                country = Country.create(
                    name=serializer.validated_data['name'],
                    user=request.infoUser.get('id')
                )
            except DatabaseError:
                country = None

            return Response(
                CountryStoreSerializer(country).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, pk):
        country = self.get_object()
        serializer = CountryDetailSerializer(
            data=request.data,
            context={"request": request, "country": country}
        )
        if serializer.is_valid():
            country.change(
                name=serializer.validated_data['name'],
                user=request.infoUser.get('id')
            )
            return Response(
                CountryDetailSerializer(
                    country,
                    context={"request": request, "country": country}
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
