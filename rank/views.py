from django.db import DatabaseError
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.http import Http404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from rank.serializers import (
    RankStoreSerializer, RankDetailSerializer,
    RankDestroySerializer, RankRestoreSerializer
)

from rank.models import Rank
from firm.models import Firm
from employee.models import Employee

from common.permissions import IsDeactivate
from rank.permissions import (
    IsAddRank, IsChangeRank, IsDestroyRank,
    IsRestoreRank, IsViewAllRank, IsViewDetailRank
)


class RankViewSet(viewsets.ModelViewSet):
    """ rank controller """

    def get_serializer_class(self):
        """ define serializer """
        if self.action in ['retrieve', 'update']:
            return RankDetailSerializer
        elif self.action == 'destroy':
            return RankDestroySerializer
        elif self.action == 'restore':
            return RankRestoreSerializer
        return RankStoreSerializer

    def get_permissions(self):
        """ define permissions """
        if self.action == 'list':
            self.permission_classes = [IsViewAllRank]
        elif self.action == 'retrieve':
            self.permission_classes = [IsViewDetailRank]
        elif self.action == 'create':
            self.permission_classes = [IsAddRank]
        elif self.action == 'update':
            self.permission_classes = [IsChangeRank]
        elif self.action == 'destroy':
            self.permission_classes = [IsDestroyRank]
        elif self.action == 'restore':
            self.permission_classes = [IsRestoreRank]
        else:
            self.permission_classes = [IsDeactivate]
        return super().get_permissions()

    def get_queryset(self):
        """ define queryset """
        if self.request.infoUser['user']['is_superuser'] is True:
            queryset = Rank.objects.all()
        else:
            queryset = Employee.ranks_visibles(
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
        """ add rank """
        serializer = RankStoreSerializer(
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            try:
                firm = Firm.readByToken(
                    token=serializer.validated_data['firm_id'])
                rank = Rank.create(
                    label=serializer.validated_data['label'],
                    power=serializer.validated_data['power'],
                    firm=firm,
                    user=request.infoUser.get('uuid')
                )
            except DatabaseError:
                rank = None

            return Response(
                RankStoreSerializer(
                    rank,
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
        rank = self.get_object()
        serializer = RankDetailSerializer(
            data=request.data,
            context={"request": request, "rank": rank}
        )
        if serializer.is_valid():
            rank.change(
                power=serializer.validated_data['power'],
                label=serializer.validated_data['label'],
                user=request.infoUser.get('uuid')
            )
            return Response(
                RankDetailSerializer(
                    rank,
                    context={"request": request, "rank": rank}
                ).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk):
        rank = self.get_object()
        serializer = RankDestroySerializer(
            data=request.data,
            context={"request": request, "rank": rank}
        )
        if serializer.is_valid():
            rank.delete(
                user=request.infoUser.get('uuid')
            )
            return Response(
                RankDestroySerializer(
                    rank,
                    context={"request": request, "rank": rank}
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
        rank = self.get_object()
        serializer = RankRestoreSerializer(
            data=request.data,
            context={"request": request, "rank": rank}
        )
        if serializer.is_valid():
            rank.restore(user=request.infoUser.get('uuid'))
            return Response(
                    RankDetailSerializer(
                        rank,
                        context={"request": request, "rank": rank}
                    ).data,
                    status=status.HTTP_200_OK
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
