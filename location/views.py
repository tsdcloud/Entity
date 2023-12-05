from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.http import Http404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

import http.client
import json

from common.permissions import IsDeactivate, IsActivate

from location.serializers import (
    CountryStoreSerializer,
    CountryDetailSerializer,
    CountryDestroySerializer,
    RegionStoreSerializer,
    RegionDetailSerializer,
    RegionDestroySerializer,
    DepartmentStoreSerializer,
    DepartementDetailSerializer,
    DepartmentDestroySerializer,
    MunicipalityStoreSerializer,
    MunicipalityDetailSerializer,
    MunicipalityDestroySerializer,
    VillageStoreSerializer,
    VillageDetailSerializer,
    VillageDestroySerializer,
    LocationStoreSerializer,
    LocationDetailSerializer
)
from location.permissions import (
    IsAddLocation,
    IsAddSite,
    IsChangeSite,
    IsDeleteSite,
    IsViewAllSite,
    IsViewDetailSite
)
from location.models import (
    Country,
    Region,
    Department,
    Municipality,
    Village,
    Location
)
from employee.models import Employee
from firm.models import Firm


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
        if self.action in ["create", "update", "destroy", "ptz"]:
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

    @action(detail=True, methods=["get"])
    def regions(self, request, pk):
        country = self.get_object()
        return Response(
            RegionStoreSerializer(
                country.regions.filter(is_active=True),
                many=True
            ).data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["get"])
    def ptz(self, request, pk=None):
        """ import countries regions departments municipalities villages """
        conn1 = http.client.HTTPSConnection('bfc.api.zukulufeg.com')
        payload1 = ''
        headers1 = {
            "Authorization": 'd3f46689-b1bc-4ab5-947b-968367a54982:04-06-2023-14-01-16'
        }
        conn1.request("GET", "/api/localite", payload1, headers1)
        response1 = conn1.getresponse()
        data = json.loads(response1.read())
        d = data['data']
        countries = d['pays']
        country = ''
        user = request.infoUser.get('id')
        for pays in countries:
            nom_pays = pays['nom']
            country = Country.create(
                name=nom_pays,
                user=request.infoUser.get('id')
            )
            regions = pays['regions']
            for item_region in regions:
                nom_region = item_region['nom']
                region = Region.create(
                    country=country,
                    name=nom_region,
                    user=user
                )
                departements = item_region['departements']
                for item_departement in departements:
                    nom_department = item_departement['nom']
                    departement = Department.create(
                        region=region,
                        name=nom_department,
                        user=user
                    )
                    communes = item_departement['communes']
                    for item_commune in communes:
                        nom_commune = item_commune['nom']
                        commune = Municipality.create(
                            department=departement,
                            name=nom_commune,
                            user=user
                        )
                        arrondissements = item_commune['arrondissements']
                        for item_arrondissement in arrondissements:
                            villages = item_arrondissement['villages']
                            for item in villages:
                                village = Village.create(
                                    municipality=commune,
                                    name=item,
                                    user=user
                                )
        return Response(
            CountryStoreSerializer(country).data,
            status=status.HTTP_201_CREATED
        )


class RegionViewSet(viewsets.ModelViewSet):
    """ region controller """

    def get_serializer_class(self):
        """ define serializer """
        if self.action in ['retrieve', 'update']:
            return RegionDetailSerializer
        elif self.action == 'destroy':
            return RegionDestroySerializer
        return RegionStoreSerializer

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


class DepartmentViewSet(viewsets.ModelViewSet):
    """ department controller """

    def get_serializer_class(self):
        """ define serializer """
        if self.action in ['retrieve', 'update']:
            return DepartementDetailSerializer
        elif self.action == 'destroy':
            return DepartmentDestroySerializer
        return DepartmentStoreSerializer

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
        queryset = Department.objects.filter(is_active=True)
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
        """ add department """
        serializer = DepartmentStoreSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            region = Region.readByToken(
                token=serializer.validated_data['region_id'])
            department = Department.create(
                name=serializer.validated_data['name'],
                user=request.infoUser.get('id'),
                region=region
            )
            return Response(
                DepartmentStoreSerializer(department).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, pk):
        department = self.get_object()
        serializer = DepartementDetailSerializer(
            data=request.data,
            context={"request": request, "department": department}
        )
        if serializer.is_valid():
            department.change(
                name=serializer.validated_data['name'],
                user=request.infoUser.get('id')
            )
            return Response(
                DepartementDetailSerializer(
                    department,
                    context={"request": request, "department": department}
                ).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk):
        department = self.get_object()
        serializer = DepartmentDestroySerializer(
            data=request.data,
            context={"request": request, "department": department}
        )
        if serializer.is_valid():
            department.delete(
                user=request.infoUser.get('id')
            )
            return Response(
                DepartmentDestroySerializer(
                    department,
                    context={"request": request, "department": department}
                ).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class MunicipalityViewSet(viewsets.ModelViewSet):
    """ municipality controller """

    def get_serializer_class(self):
        """ define serializer """
        if self.action in ['retrieve', 'update']:
            return MunicipalityDetailSerializer
        elif self.action == 'destroy':
            return MunicipalityDestroySerializer
        return MunicipalityStoreSerializer

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
        queryset = Municipality.objects.filter(is_active=True)
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
        """ add municipality """
        serializer = MunicipalityStoreSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            department = Department.readByToken(
                token=serializer.validated_data['department_id'])
            municipality = Municipality.create(
                name=serializer.validated_data['name'],
                user=request.infoUser.get('id'),
                department=department
            )
            return Response(
                MunicipalityStoreSerializer(municipality).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, pk):
        municipality = self.get_object()
        serializer = MunicipalityDetailSerializer(
            data=request.data,
            context={"request": request, "municipality": municipality}
        )
        if serializer.is_valid():
            municipality.change(
                name=serializer.validated_data['name'],
                user=request.infoUser.get('id')
            )
            return Response(
                MunicipalityDetailSerializer(
                    municipality,
                    context={"request": request, "municipality": municipality}
                ).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk):
        municipality = self.get_object()
        serializer = MunicipalityDestroySerializer(
            data=request.data,
            context={"request": request, "municipality": municipality}
        )
        if serializer.is_valid():
            municipality.delete(
                user=request.infoUser.get('id')
            )
            return Response(
                MunicipalityDestroySerializer(
                    municipality,
                    context={"request": request, "municipality": municipality}
                ).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class VillageViewSet(viewsets.ModelViewSet):
    """ village controller """

    def get_serializer_class(self):
        """ define serializer """
        if self.action in ['retrieve', 'update']:
            return VillageDetailSerializer
        elif self.action == 'destroy':
            return VillageDestroySerializer
        return VillageStoreSerializer

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
        queryset = Village.objects.filter(is_active=True)
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
        """ add village """
        serializer = VillageStoreSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            municipality = Municipality.readByToken(
                token=serializer.validated_data['municipality_id'])
            village = Village.create(
                name=serializer.validated_data['name'],
                user=request.infoUser.get('id'),
                municipality=municipality
            )
            return Response(
                VillageStoreSerializer(village).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, pk):
        village = self.get_object()
        serializer = VillageDetailSerializer(
            data=request.data,
            context={"request": request, "village": village}
        )
        if serializer.is_valid():
            village.change(
                name=serializer.validated_data['name'],
                user=request.infoUser.get('id')
            )
            return Response(
                VillageDetailSerializer(
                    village,
                    context={"request": request, "village": village}
                ).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk):
        village = self.get_object()
        serializer = VillageDestroySerializer(
            data=request.data,
            context={"request": request, "village": village}
        )
        if serializer.is_valid():
            village.delete(
                user=request.infoUser.get('id')
            )
            return Response(
                VillageDestroySerializer(
                    village,
                    context={"request": request, "village": village}
                ).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class LocationViewSet(viewsets.ModelViewSet):
    """ location controller """

    def get_serializer_class(self):
        """ define serializer """
        if self.action in ['retrieve', 'update']:
            return LocationDetailSerializer
        else:
            return LocationStoreSerializer

    def get_permissions(self):
        """ define permissions """
        if self.action == 'create':
            self.permission_classes = [IsAddSite]
        elif self.action == 'list':
            self.permission_classes = [IsViewAllSite]
        elif self.action == 'retrieve':
            self.permission_classes = [IsViewDetailSite]
        elif self.action == 'update':
            self.permission_classes = [IsChangeSite]
        elif self.action == 'destroy':
            self.permission_classes = [IsDeleteSite]
        else:
            self.permission_classes = [IsDeactivate]
        return super().get_permissions()

    def get_queryset(self):
        """ define queryset """
        queryset = Employee.sites_visibles(
            user=self.request.infoUser.get('id'),
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
        """ add location """
        serializer = LocationStoreSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            firm = Firm.readByToken(token=serializer.validated_data['firm_id'])
            village = Village.readByToken(
                token=serializer.validated_data['village_id'])
            location = Location.create(
                firm=firm,
                village=village,
                name=serializer.validated_data['name'],
                user=request.infoUser.get('id')
            )
            return Response(
                LocationStoreSerializer(location).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, pk):
        location = self.get_object()
        serializer = LocationDetailSerializer(
            data=request.data,
            context={"request": request, "location": location}
        )
        if serializer.is_valid():
            location.change(
                name=serializer.validated_data['name'],
                user=request.infoUser.get('id')
            )
            return Response(
                LocationDetailSerializer(
                    location,
                    context={"request": request, "location": location}
                ).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk):
        location = self.get_object()
        location.delete(
            user=request.infoUser.get('id')
        )
        return Response(
            LocationDetailSerializer(
                location,
                context={"request": request, "location": location}
            ).data,
            status=status.HTTP_200_OK
        )
