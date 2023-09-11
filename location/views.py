from django.db import DatabaseError
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.http import Http404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from common.permissions import IsDeactivate, IsActivate

from location.serializers import (
    CountryStoreSerializer,
    CountryDetailSerializer,
    CountryDestroySerializer,
    RegionStoreSerializer,
    RegionDetailSerializer,
    RegionDestroySerializer
)
from location.permissions import (
    IsAddLocation
)
from location.models import (
    Country,
    Region
)


class CountryViewSet(viewsets.ModelViewSet):
    """ country controller """

    def get_serializer_class(self):
        """ define serializer """
        if self.action in ['retrieve', 'update']:
            return CountryDetailSerializer
        elif self.action == 'destroy':
            return CountryDestroySerializer
        return CountryStoreSerializer

    def get_permissions(self):
        """ define permissions """
        if self.action in ["create", "update", "destroy"]:
            self.permission_classes = [IsAddLocation]
        elif self.action in ["list", "retrieve"]:
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
            country = Country.create(
                name=serializer.validated_data['name'],
                user=request.infoUser.get('id')
            )
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
        country = self.get_object()
        serializer = CountryDestroySerializer(
            data=request.data,
            context={"request": request, "country": country}
        )
        if serializer.is_valid():
            country.delete(
                user=request.infoUser.get('id')
            )
            return Response(
                CountryDestroySerializer(
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


class RegionViewSet(viewsets.ModelViewSet):
    """ region controller """

    def get_serializer_class(self):
        """ define serializer """
        if self.action in ['retrieve', 'update']:
            return RegionDetailSerializer
        elif self.action == 'destroy':
            return RegionDestroySerializer
        return CountryStoreSerializer

    def get_permissions(self):
        """ define permissions """
        if self.action in ["create", "update", "destroy"]:
            self.permission_classes = [IsAddLocation]
        elif self.action in ["list", "retrieve"]:
            self.permission_classes = [IsActivate]
        else:
            self.permission_classes = [IsDeactivate]
        return super().get_permissions()

    def get_queryset(self):
        """ define queryset """
        queryset = Region.objects.filter(is_active=True)
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
        """ add region """
        serializer = RegionStoreSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            country = Country.readByToken(
                token=serializer.validated_data['country_id'])
            region = Region.create(
                name=serializer.validated_data['name'],
                user=request.infoUser.get('id'),
                country=country
            )
            return Response(
                RegionStoreSerializer(region).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, pk):
        region = self.get_object()
        serializer = RegionDetailSerializer(
            data=request.data,
            context={"request": request, "region": region}
        )
        if serializer.is_valid():
            region.change(
                name=serializer.validated_data['name'],
                user=request.infoUser.get('id')
            )
            return Response(
                RegionDetailSerializer(
                    region,
                    context={"request": request, "region": region}
                ).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk):
        region = self.get_object()
        serializer = RegionDestroySerializer(
            data=request.data,
            context={"request": request, "region": region}
        )
        if serializer.is_valid():
            region.delete(
                user=request.infoUser.get('id')
            )
            return Response(
                RegionDestroySerializer(
                    region,
                    context={"request": request, "region": region}
                ).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
