from rest_framework import serializers

from firm.models import Firm
from branch.models import Branch

from firm.serializers import FirmPartialSerializer


class BranchStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add branch """
    id = serializers.CharField(read_only=True)
    is_service = serializers.BooleanField(read_only=True)
    is_principal = serializers.BooleanField(read_only=True)

    origin = serializers.SerializerMethodField()
    firm = FirmPartialSerializer(many=False)

    class Meta:
        """ attributs serialized """
        model = Branch
        fields = [
            'id',
            'is_service',
            'is_principal',
            'label',
            'origin',
            'firm'
        ]

    def get_origin(self, instance):
        """ serialize origin """
        if instance.is_principal is True:
            id = instance.id
        else:
            id = instance.origin.id
        res = {
            "id": id,
            "label": instance.label
        }
        return res

    def validate_origin(self, value):
        """ check validity of origin """
        try:
            Branch.objects.get(id=value, is_active=True)
        except Branch.DoesNotExist:
            raise serializers.ValidationError('origin not found')
        return value

    def validate_firm(self, value):
        """ check validity of firm """
        try:
            Firm.objects.get(id=value, is_active=True)
        except Firm.DoesNotExist:
            raise serializers.ValidationError('firm not found')
        return value

    def validate(self, data):
        """ check logical validation """
        firm = Firm.objects.get(id=data['firm'])
        origin = Branch.objects.get(id=data['branch'])
        if firm != origin.firm:
            raise serializers.ValidationError('firm and origin not found')
        try:
            Branch.objects.get(label=data['label'].upper(), firm=firm)
            raise serializers.ValidationError('label already exists')
        except Branch.DoesNotExist:
            pass
        return data


class BranchDetailSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for update branch """
    id = serializers.CharField(read_only=True)
    is_service = serializers.BooleanField(read_only=True)
    is_principal = serializers.BooleanField(read_only=True)
    date = serializers.DateTimeField(read_only=True)

    origin = serializers.SerializerMethodField()
    firm = FirmPartialSerializer(many=False)

    class Meta:
        """ attributs serialized """
        model = Branch
        fields = "__all__"

    def get_origin(self, instance):
        """ serialize origin """
        if instance.is_principal is True:
            id = instance.id
        else:
            id = instance.origin.id
        res = {
            "id": id,
            "label": instance.label
        }
        return res

    def validate_origin(self, value):
        """ check validity of origin """
        try:
            Branch.objects.get(id=value, is_active=True)
        except Branch.DoesNotExist:
            raise serializers.ValidationError('origin not found')
        return value

    def validate_firm(self, value):
        """ check validity of firm """
        try:
            Firm.objects.get(id=value, is_active=True)
        except Firm.DoesNotExist:
            raise serializers.ValidationError('firm not found')
        return value

    def validate(self, data):
        """ check logical validation """
        firm = Firm.objects.get(id=data['firm'])
        origin = Branch.objects.get(id=data['branch'])
        if firm != origin.firm:
            raise serializers.ValidationError('firm and origin not found')
        try:
            Branch.objects.get(label=data['label'].upper(), firm=firm)
            raise serializers.ValidationError('label already exists')
        except Branch.DoesNotExist:
            pass
        return data
