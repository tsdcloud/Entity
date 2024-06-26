from rest_framework import serializers

from firm.models import Firm

from .constants import ACCEPT_IMAGE, MAX_IMAGE_SIZE

import base64
import io

from PIL import Image


class FirmStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add entity """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    tax_reporting_center = serializers.CharField(
        max_length=50)
    trade_register = serializers.CharField(
        max_length=50)

    class Meta:
        """ attributs serialized """
        model = Firm
        fields = [
            'business_name',
            'acronym',
            'unique_identifier_number',
            'principal_activity',
            'regime',
            'tax_reporting_center',
            'trade_register',
            'logo',
            'type_person',
            'id',
            'is_active'
        ]

    def validate_business_name(self, value):
        """ check validity of business_name """
        try:
            Firm.objects.get(business_name=value.upper())
            raise serializers.ValidationError('business_name already exists')
        except Firm.DoesNotExist:
            return value

    def validate_unique_identifier_number(self, value):
        """ check validity of unique identifier number """
        if len(value) != 14:
            raise serializers.ValidationError(
                'wrong unique_identifier_number size'
            )
        try:
            Firm.objects.get(unique_identifier_number=value.upper())
            raise serializers.ValidationError(
                'unique_identifier_number already exists'
            )
        except Firm.DoesNotExist:
            return value

    def validate_trade_register(self, value):
        """ check validity of trade_register """
        try:
            Firm.objects.get(trade_register=value.upper())
            raise serializers.ValidationError('trade_register already exists')
        except Firm.DoesNotExist:
            return value

    def validate_type_person(self, value):
        """ check validity of type_person """
        if value not in [1, 2, '1', '2']:
            raise serializers.ValidationError(
                'provide correct value for type_person')
        return value

    def validate_logo(self, value):
        """ check validity of logo """
        try:
            image = base64.b64decode(value)
            img = Image.open(io.BytesIO(image))
        except Exception:
            raise serializers.ValidationError('logo is not valid base64 image')
        if img.format.lower() in ACCEPT_IMAGE:
            width, height = img.size
            if width * height > MAX_IMAGE_SIZE:
                raise serializers.ValidationError('image too large')
        else:
            raise serializers.ValidationError('not valid extension')
        return value


class FirmDetailSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for update entity """
    id = serializers.CharField(
        max_length=1000, required=False, read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    date = serializers.DateTimeField(read_only=True)
    business_name = serializers.CharField()
    unique_identifier_number = serializers.CharField()
    tax_reporting_center = serializers.CharField(
        max_length=50)
    trade_register = serializers.CharField(
        max_length=50)

    class Meta:
        """ attributs serialized """
        model = Firm
        fields = "__all__"

    def validate_business_name(self, value):
        """ check validity of social_raison """
        try:
            f = Firm.objects.get(business_name=value.upper())
            firm = self.context['firm']
            if f != firm:
                raise serializers.ValidationError(
                    'business_name already exists'
                )
            else:
                return value
        except Firm.DoesNotExist:
            return value

    def validate_unique_identifier_number(self, value):
        """ check validity of unique_identifier_number """
        try:
            f = Firm.objects.get(unique_identifier_number=value.upper())
            firm = self.context['firm']
            if f != firm:
                raise serializers.ValidationError(
                    'unique_identifier_number already exists'
                )
            elif len(value) != 14:
                raise serializers.ValidationError(
                    'wrong unique_identifier_number size'
                )
            else:
                return value
        except Firm.DoesNotExist:
            return value

    def validate_trade_register(self, value):
        """ check validity of trade_register """
        try:
            f = Firm.objects.get(trade_register=value.upper())
            firm = self.context['firm']
            if f != firm:
                raise serializers.ValidationError(
                    'trade_register already exists'
                )
            else:
                return value
        except Firm.DoesNotExist:
            return value

    def validate_type_person(self, value):
        """ check validity of type_person """
        if value not in [1, 2, '1', '2']:
            raise serializers.ValidationError(
                'provide correct value for type_person'
            )
        return value

    def validate_logo(self, value):
        """ check validity of logo """
        try:
            image = base64.b64decode(value)
            img = Image.open(io.BytesIO(image))
        except Exception:
            raise serializers.ValidationError('logo is not valid base64 image')
        if img.format.lower() in ACCEPT_IMAGE:
            width, height = img.size
            if width * height > MAX_IMAGE_SIZE:
                raise serializers.ValidationError('image too large')
        else:
            raise serializers.ValidationError('not valid extension')
        return value
