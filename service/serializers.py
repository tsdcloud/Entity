from rest_framework import serializers

from service.models import Service
from branch.models import Branch
from employee.models import Employee


class ServiceStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add service """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    branch = serializers.SerializerMethodField(read_only=True)
    branch_id = serializers.CharField(write_only=True, max_length=1000)
    description = serializers.CharField(required=False, max_length=2000)

    class Meta:
        """ attributs serialized """
        model = Service
        fields = [
            'name',
            'description',
            'branch_id',
            'branch',
            'is_active',
            'id'
        ]

    def get_branch(self, instance):
        return {
            "id": instance.branch.id,
            "label": instance.branch.label,
            "is_principal": instance.branch.is_principal
        }

    def validate_branch_id(self, value):
        """ check validity of branch_id """
        try:
            Branch.objects.get(id=value, is_active=True, is_service=False)
        except Branch.DoesNotExist:
            raise serializers.ValidationError(
                detail='branch_id not found', code=-1
            )
        return value

    def validate(self, data):
        branch = Branch.objects.get(id=data['branch_id'])
        firm = branch.firm
        try:
            Service.objects.get(
                name=data['name'].upper(),
                is_active=True,
                branch_firm=firm
            )
            raise serializers.ValidationError(
                detail="name already exists", code=-1
            )
        except Service.DoesNotExist:
            return data


class ServiceDetailSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for update service """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    date = serializers.DateTimeField(read_only=True)
    branch = serializers.SerializerMethodField(read_only=True)
    branch_id = serializers.CharField(write_only=True, max_length=1000)
    description = serializers.CharField(required=False, max_length=2000)

    class Meta:
        """ attributs serialized """
        model = Service
        fields = "__all__"

    def get_branch(self, instance):
        return {
            "id": instance.branch.id,
            "label": instance.branch.label,
            "is_principal": instance.branch.is_principal
        }

    def validate_name(self, value):
        """ check validity of name """
        service = self.context['service']
        try:
            s = Service.objects.get(
                name=value.upper(),
                branch__firm=service.branch.firm,
                is_active=True
            )
            if service != s:
                raise serializers.ValidationError(
                    detail='name already exists', code=-1
                )
        except Service.DoesNotExist:
            return value

    def validate_branch_id(self, value):
        """ check validity of branch_id """
        service = self.context['service']
        try:
            branch = Branch.objects.get(id=value, is_active=True)
            if branch.is_service is True and branch != service.branch:
                raise serializers.ValidationError(
                    detail="branch not available",
                    code=-1
                )
        except Branch.DoesNotExist:
            raise serializers.ValidationError(
                detail='branch_id not found',
                code=-1
            )
        return value


class ServiceDestroySerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for delete service """
    id = serializers.CharField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Branch
        fields = "id"

    def validate(self, data):
        """ check logical validation """
        service = self.context['service']
        employees = Employee.objects.filter(
            function__service=service,
            is_active=True
        )
        if len(employees) != 0:
            raise serializers.ValidationError(
                detail='This service constains a valid personels',
                code=-1
            )
        return data


class ServiceRestoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for restore service """
    id = serializers.CharField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Branch
        fields = "id"

    def validate(self, data):
        """ check logical validation """
        service = self.context['service']
        if service.branch.is_service is True:
            raise serializers.ValidationError(
                'cant not restore this service ' +
                'because this branch is used by ' +
                'another service'
            )
        return data
