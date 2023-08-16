from rest_framework import serializers

from employee.models import Employee
from rank.models import Rank
from function.models import Function
from common.constants import EMPLOYEE_CATEGORIE


class EmployeeStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add employee """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    user_id = serializers.CharField(max_length=1000, write_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    category = serializers.ChoiceField(choices=EMPLOYEE_CATEGORIE)
    rank_id = serializers.CharField(max_length=1000, write_only=True)
    rank = serializers.SerializerMethodField(read_only=True)
    function_id = serializers.CharField(max_length=1000, write_only=True)
    function = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Employee
        fields = [
            'id',
            'is_active',
            'user_id',
            'user',
            'category',
            'rank_id',
            'rank',
            'function_id',
            'function'
        ]

    def get_user(self, instance):
        instance.decryptuser(
            authorization=self.context['request'].headers.get('Authorization')
        )
        return instance.utilisateur

    def get_rank(self, instance):
        return {
            "id": instance.rank.id,
            "label": instance.rank.label,
            "power": instance.rank.power
        }

    def get_function(self, instance):
        return {
            "id": instance.function.id,
            "label": instance.function.label,
            "power": instance.function.power
        }

    def validate_user_id(self, value):
        """ check validity of user_id """
        data = Employee.get_user(
            user=value,
            authorization=self.context['request'].headers.get(
                'Authorization'
            )
        )
        if data is None:
            raise serializers.ValidationError(
                detail='user not found',
                code=-1
            )
        return value

    def validate_rank_id(self, value):
        """ check validity of rank_id """
        try:
            Rank.objects.get(id=value, is_active=True)
        except Rank.DoesNotExist:
            raise serializers.ValidationError(
                detail='rank_id not found',
                code=-1
            )
        return value

    def validate_function_id(self, value):
        """ check validity of function_id """
        try:
            Function.objects.get(id=value, is_active=True)
        except Function.DoesNotExist:
            raise serializers.ValidationError(
                detail='function_id not found',
                code=-1
            )
        return value

    def validate(self, data):
        function = Function.readByToken(token=data['function_id'])
        rank = Rank.readByToken(token=data['rank_id'])
        user = Employee.get_user(
            user=data['user_id'],
            authorization=self.context['request'].headers.get(
                'Authorization'
            )
        )
        if rank.firm != function.service.branch.firm:
            raise serializers.ValidationError(
                detail='not found',
                code=-2
            )
        try:
            Employee.objects.get(
                user=user['uuid'],
                rank__firm=rank.firm, is_active=True
            )
            raise serializers.ValidationError(
                detail='user not found',
                code=-2
            )
        except Employee.DoesNotExist:
            return data


class EmployeeDetailSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for update employee """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    category = serializers.ChoiceField(choices=EMPLOYEE_CATEGORIE)
    rank_id = serializers.CharField(max_length=1000, write_only=True)
    rank = serializers.SerializerMethodField(read_only=True)
    function_id = serializers.CharField(max_length=1000, write_only=True)
    function = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Employee
        fields = [
            'id',
            'is_active',
            'user',
            'category',
            'rank_id',
            'rank',
            'function_id',
            'function'
        ]

    def get_user(self, instance):
        instance.decryptuser(
            authorization=self.context['request'].headers.get('Authorization')
        )
        return instance.utilisateur

    def get_rank(self, instance):
        return {
            "id": instance.rank.id,
            "label": instance.rank.label,
            "power": instance.rank.power
        }

    def get_function(self, instance):
        return {
            "id": instance.function.id,
            "label": instance.function.label,
            "power": instance.function.power
        }

    def validate_rank_id(self, value):
        """ check validity of rank_id """
        try:
            Rank.objects.get(id=value, is_active=True)
        except Rank.DoesNotExist:
            raise serializers.ValidationError(
                detail='rank_id not found',
                code=-1
            )
        return value

    def validate_function_id(self, value):
        """ check validity of function_id """
        try:
            Function.objects.get(id=value, is_active=True)
        except Function.DoesNotExist:
            raise serializers.ValidationError(
                detail='function_id not found',
                code=-1
            )
        return value

    def validate(self, data):
        function = Function.readByToken(token=data['function_id'])
        rank = Rank.readByToken(token=data['rank_id'])
        if rank.firm != function.service.branch.firm:
            raise serializers.ValidationError(
                detail='not found',
                code=-2
            )
        return data
