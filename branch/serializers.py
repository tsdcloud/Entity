from rest_framework import serializers

from firm.models import Firm
from branch.models import Branch


class BranchStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add branch """
    id = serializers.CharField(read_only=True)
    is_service = serializers.BooleanField(read_only=True)
    is_principal = serializers.BooleanField(read_only=True)

    origin_id = serializers.CharField(
        max_length=1000, write_only=True)
    firm_id = serializers.CharField(
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
            'origin_id',
            'firm_id'
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

    def validate_origin_id(self, value):
        """ check validity of origin_id """
        try:
            Branch.objects.get(id=value, is_active=True)
        except Branch.DoesNotExist:
            raise serializers.ValidationError('origin_id not found')
        return value

    def validate_firm_id(self, value):
        """ check validity of firm_id """
        try:
            Firm.objects.get(id=value, is_active=True)
        except Firm.DoesNotExist:
            raise serializers.ValidationError('firm_id not found')
        return value

    def validate(self, data):
        """ check logical validation """
        firm = Firm.objects.get(id=data['firm_id'])
        origin = Branch.objects.get(id=data['origin_id'])
        if firm != origin.firm:
            raise serializers.ValidationError(
                detail='firm_id and origin_id not found',
                code=-1
            )
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

    origin_id = serializers.CharField(
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

    def validate_origin_id(self, value):
        """ check validity of origin_id """
        try:
            Branch.objects.get(id=value, is_active=True)
        except Branch.DoesNotExist:
            raise serializers.ValidationError('origin_id not found')
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
        origin = Branch.objects.get(id=data['origin_id'])
        if branch.firm != origin.firm:
            raise serializers.ValidationError('provide a good origin_id ')
        if branch == origin:
            raise serializers.ValidationError(
                'provide a valid origin_id for this branch'
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


class BranchDestroySerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for delete branch """
    id = serializers.CharField(read_only=True)
    is_service = serializers.BooleanField(read_only=True)
    is_principal = serializers.BooleanField(read_only=True)
    date = serializers.DateTimeField(read_only=True)

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

    def validate(self, data):
        """ check logical validation """
        branch = self.context['branch']
        if branch.is_active is False:
            raise serializers.ValidationError(
                'branch is not active'
            )
        if branch.is_principal is True:
            raise serializers.ValidationError(
                'cant not delete this branch'
            )
        if branch.is_service is True:
            raise serializers.ValidationError(
                'cant not delete this branch ' +
                'because this branch is used by ' +
                'an service'
            )

        tb = Branch.objects.filter(
            origin=branch,
            is_active=True
        )
        if 0 != len(tb):
            raise serializers.ValidationError(
                'you cant not delete this branch,' +
                'because, this branch is used by ' +
                'an other branch'
            )
        return data


class BranchRestoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for restore branch """
    id = serializers.CharField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Branch
        fields = "id"

    def validate(self, data):
        """ check logical validation """
        branch = self.context['branch']
        if branch.is_principal is True:
            raise serializers.ValidationError(
                detail='You cannot restore this branch',
                code=-1
            )
        elif branch.origin.is_active is False:
            raise serializers.ValidationError(
                'cant not restore this branch ' +
                'because this branch has not ' +
                'a valid origin'
            )
        return data
