from rest_framework import serializers

from employee.models import Employee
from firm.models import Firm
from rank.models import Rank


class RankStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add rank """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    firm = serializers.SerializerMethodField(read_only=True)
    firm_id = serializers.CharField(write_only=True, max_length=1000)

    class Meta:
        """ attributs serialized """
        model = Rank
        fields = [
            'label',
            'power',
            'firm',
            'firm_id',
            'is_active',
            'id'
        ]

    def get_firm(self, instance):
        return {
            "id": instance.firm.id,
            "business_name": instance.firm.business_name,
            "acronym": instance.firm.acronym
        }

    def validate_firm_id(self, value):
        """ check validity of firm_id """
        try:
            Firm.objects.get(id=value, is_active=True)
        except Firm.DoesNotExist:
            raise serializers.ValidationError(
                detail='firm_id not found', code=-1
            )
        return value

    def validate_power(self, value):
        """ check validity of power """
        if value < 1:
            raise serializers.ValidationError(
                detail='power is not valid', code=-1
            )
        return value

    def validate(self, data):
        firm = Firm.objects.get(id=data['firm_id'])
        label = data['label']
        request = self.context['request']
        is_superuser = request.infoUser['user']['is_superuser']
        firms_possibles = Employee.firms_visibles(
            user=request.infoUser['uuid'],
            is_superuser=is_superuser
        )
        if firm not in firms_possibles:
            raise serializers.ValidationError(
                detail="firm not found",
                code=-2
            )
        try:
            Rank.objects.get(
                label=label.upper(),
                is_active=True,
                firm=firm
            )
            raise serializers.ValidationError(
                detail="name already exists", code=-1
            )
        except Rank.DoesNotExist:
            return data


class RankDetailSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for update rank """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    date = serializers.DateTimeField(read_only=True)
    firm = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Rank
        fields = "__all__"

    def get_firm(self, instance):
        return {
            "id": instance.firm.id,
            "business_name": instance.firm.business_name,
            "acronym": instance.firm.acronym
        }

    def validate_label(self, value):
        """ check validity of label """
        rank = self.context['rank']
        try:
            r = Rank.objects.get(
                label=value.upper(),
                firm=rank.firm
            )
            if r != rank:
                raise serializers.ValidationError(
                    detail='name already exists', code=-1
                )
        except Rank.DoesNotExist:
            pass
        return value

    def validate_power(self, value):
        """ check validity of power """
        if value < 1:
            raise serializers.ValidationError(
                detail='power is not valid', code=-1
            )
        return value


class RankDestroySerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for delete rank """
    id = serializers.CharField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Rank
        fields = ["id"]

    def validate(self, data):
        """ check logical validation """
        rank = self.context['rank']
        employees = Employee.objects.filter(
            rank=rank,
            is_active=True
        )
        if len(employees) != 0:
            raise serializers.ValidationError(
                detail='This rank constains a valid personels',
                code=-1
            )
        return data


class RankRestoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for restore rank """
    id = serializers.CharField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Rank
        fields = ["id"]

    def validate(self, data):
        """ check logical validation """
        rank = self.context['rank']
        if rank.firm.is_active is False:
            raise serializers.ValidationError(
                'cant not restore this rank ' +
                'because her firm is not available'
            )
        return data
