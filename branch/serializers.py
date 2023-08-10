from rest_framework import serializers

from firm.models import Firm
from branch.models import Branch


class BranchStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add branch """
    id = serializers.CharField(read_only=True)
    is_service = serializers.BooleanField(read_only=True)
    is_principal = serializers.BooleanField(read_only=True)

    start = serializers.CharField(
        max_length=1000, write_only=True)
    entity = serializers.CharField(
        max_length=1000, write_only=True)

    origin = serializers.SerializerMethodField(read_only=True)
    firm = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Branch
        fields = [
            'id',
            'is_service',
            'is_principal',
            'label',
            'origin',
            'firm',
            'start',
            'entity'
        ]

    def get_origin(self, instance):
        """ serialize origin """
        if instance.is_principal is True:
            id = instance.id
            label = instance.label
        else:
            id = instance.origin.id
            label = instance.origin.label
        res = {
            "id": id,
            "label": label
        }
        return res

    def get_firm(self, instance):
        return {
            "id": instance.firm.id,
            "business_name": instance.firm.business_name,
            "acronym": instance.firm.acronym,
            "logo": instance.firm.logo
        }

    def validate_start(self, value):
        """ check validity of start """
        try:
            Branch.objects.get(id=value, is_active=True)
        except Branch.DoesNotExist:
            raise serializers.ValidationError('start not found')
        return value

    def validate_entity(self, value):
        """ check validity of entity """
        try:
            Firm.objects.get(id=value, is_active=True)
        except Firm.DoesNotExist:
            raise serializers.ValidationError('entity not found')
        return value

    def validate(self, data):
        """ check logical validation """
        firm = Firm.objects.get(id=data['entity'])
        origin = Branch.objects.get(id=data['start'])
        if firm != origin.firm:
            raise serializers.ValidationError('entity and start not found')
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

    start = serializers.CharField(
        max_length=1000, write_only=True)

    origin = serializers.SerializerMethodField(read_only=True)
    firm = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Branch
        fields = "__all__"

    def get_origin(self, instance):
        """ serialize origin """
        if instance.is_principal is True:
            id = instance.id
            label = instance.label
        else:
            id = instance.origin.id
            label = instance.origin.label
        res = {
            "id": id,
            "label": label
        }
        return res

    def get_firm(self, instance):
        return {
            "id": instance.firm.id,
            "business_name": instance.firm.business_name,
            "acronym": instance.firm.acronym,
            "logo": instance.firm.logo
        }

    def validate_start(self, value):
        """ check validity of start """
        try:
            Branch.objects.get(id=value, is_active=True)
        except Branch.DoesNotExist:
            raise serializers.ValidationError('start not found')
        return value

    def validate(self, data):
        """ check logical validation """
        branch = self.context['branch']
        if branch.is_active is False:
            raise serializers.ValidationError(
                'branch is not active'
            )
        if branch.is_principal is True:
            raise serializers.ValidationError(
                'cant not update this branch'
            )
        origin = Branch.objects.get(id=data['start'])
        if branch.firm != origin.firm:
            raise serializers.ValidationError('provide a good start ')
        if branch == origin:
            raise serializers.ValidationError(
                'provide a valid start for this branch'
            )
        try:
            tb = Branch.objects.get(
                label=data['label'].upper(),
                firm=branch.firm
            )
            if tb != branch:
                raise serializers.ValidationError('label already exists')
        except Branch.DoesNotExist:
            pass
        return data
