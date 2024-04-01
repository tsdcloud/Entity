from rest_framework import serializers
from django.contrib.auth.models import Permission

from service.models import Service
from employee.models import Employee
from function.models import Function


class FunctionStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add function """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    service = serializers.SerializerMethodField(read_only=True)
    service_id = serializers.CharField(write_only=True, max_length=1000)
    description = serializers.CharField(required=True, max_length=2000)

    class Meta:
        """ attributs serialized """
        model = Function
        fields = [
            'name',
            'description',
            'power',
            'service',
            'service_id',
            'is_active',
            'id'
        ]

    def get_service(self, instance):
        return {
            "id": instance.service.id,
            "name": instance.service.name
        }

    def validate_service_id(self, value):
        """ check validity of service_id """
        try:
            Service.objects.get(id=value, is_active=True)
        except Service.DoesNotExist:
            raise serializers.ValidationError(
                detail='service_id not found', code=-1
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
        service = Service.objects.get(id=data['service_id'])
        firm = service.branch.firm
        request = self.context['request']
        is_superuser = request.infoUser['user']['is_superuser']
        firms_visibles = Employee.firms_visibles(
            user=request.infoUser['uuid'],
            is_superuser=is_superuser
        )
        if firm not in firms_visibles:
            raise serializers.ValidationError(
                detail='no found',
                code=-2
            )
        try:
            Function.objects.get(
                name=data['name'].upper(),
                is_active=True,
                service__branch__firm=firm
            )
            raise serializers.ValidationError(
                detail="name already exists", code=-1
            )
        except Function.DoesNotExist:
            return data


class FunctionDetailSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for update function """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    date = serializers.DateTimeField(read_only=True)
    service = serializers.SerializerMethodField(read_only=True)
    permissions = serializers.SerializerMethodField(read_only=True)
    service_id = serializers.CharField(write_only=True, max_length=1000)
    description = serializers.CharField(required=True, max_length=2000)

    class Meta:
        """ attributs serialized """
        model = Function
        fields = "__all__"

    def get_service(self, instance):
        return {
            "id": instance.service.id,
            "name": instance.service.name
        }

    def get_permissions(self, instance):
        res = []
        for permission in instance.permissions.all():
            res.append({
                "codename": permission.codename,
                "desc": permission.name
            })
        return res

    def validate_name(self, value):
        """ check validity of name """
        function = self.context['function']
        try:
            f = Function.objects.get(
                name=value.upper(),
                service__branch__firm=function.service.branch.firm
            )
            if f != function:
                raise serializers.ValidationError(
                    detail='name already exists', code=-1
                )
        except Function.DoesNotExist:
            return value

    def validate_service_id(self, value):
        """ check validity of service_id """
        function = self.context['function']
        try:
            service = Service.objects.get(id=value, is_active=True)
            if service.branch.firm != function.service.branch.firm:
                raise serializers.ValidationError(
                    detail='no found',
                    code=-2
                )
        except Service.DoesNotExist:
            raise serializers.ValidationError(
                detail='service not found',
                code=-1
            )
        return value

    def validate_power(self, value):
        """ check validity of power """
        if value < 1:
            raise serializers.ValidationError(
                detail='power is not valid', code=-1
            )
        return value


class FunctionDestroySerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for delete function """
    id = serializers.CharField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Function
        fields = ["id"]

    def validate(self, data):
        """ check logical validation """
        function = self.context['function']
        employees = Employee.objects.filter(
            functions=function,
            is_active=True
        )
        if len(employees) != 0:
            raise serializers.ValidationError(
                detail='This function constains a valid personels',
                code=-1
            )
        return data


class FunctionRestoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for restore function """
    id = serializers.CharField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Function
        fields = ["id"]

    def validate(self, data):
        """ check logical validation """
        function = self.context['function']
        if function.service.is_active is False:
            raise serializers.ValidationError(
                'cant not restore this function ' +
                'because his service is not available'
            )
        return data


class FunctionAddPermissionSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for restore function """
    id = serializers.CharField(read_only=True)
    permissions = serializers.ListField(
        child=serializers.CharField(max_length=1000),
        allow_empty=True
    )

    class Meta:
        """ attributs serialized """
        model = Function
        fields = ["id", "permissions"]

    def validate_permissions(self, data):
        """ check logical validation """
        for value in data:
            try:
                Permission.objects.get(codename=value)
            except Permission.DoesNotExist:
                raise serializers.ValidationError(
                    detail="Permission not found"
                )
        return data
