from rest_framework import serializers

from firm.models import Firm

from . constances import ACCEPT_IMAGE, MAX_IMAGE_SIZE, TAX_SYSTEM



import base64, io
from PIL import Image


class FirmStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add entity """
    uuid = serializers.CharField(max_length=1000, required=False, read_only=True)
    tax_reporting_center = serializers.CharField(max_length=50, write_only=True)
    trade_register = serializers.CharField(max_length=18, write_only=True)

    class Meta:
        """ attributs serialized """
        model = Firm
        fields = ['social_raison', 'sigle', 'niu', 'principal_activity', 'regime', 'tax_reporting_center', 'trade_register', 'logo', 'type_person', 'uuid']

    def validate_social_raison(self, value):
        """ check validity of social_raison """
        try:
            Firm.objects.get(social_raison=value.upper())
            raise serializers.ValidationError('social_raison already exists')
        except Firm.DoesNotExist:
            return value

    def validate_niu(self, value):
        """ check validity of niu """
        if len(value) != 14:
            raise serializers.ValidationError('wrong niu size')
        try:
            Firm.objects.get(niu=value.upper())
            raise serializers.ValidationError('niu already exists')
        except Firm.DoesNotExist:
            return value

    def validate_trade_register(self, value):
        """ check validity of trade_register """
        if len(value) != 18:
            raise serializers.ValidationError('wrong trade_register size')
        try:
            Firm.objects.get(trade_register=value.upper())
            raise serializers.ValidationError('trade_register already exists')
        except Firm.DoesNotExist:
            return value

    def validate_type_person(self, value):
        """ check validity of type_person """
        if value not in [1,2,'1','2']:
            raise serializers.ValidationError('provide correct value for type_person')
        return value

    def validate_logo(self, value):
        """ check validity of logo """
        try:
            image = base64.b64decode(value)
            img = Image.open(io.BytesIO(image))
            if img.format.lower() in ACCEPT_IMAGE:
                width, height = img.size
                if width * height > MAX_IMAGE_SIZE:
                    raise serializers.ValidationError('image too large')
            else:
                raise serializers.ValidationError('not valid extension')
        except Exception:
            raise serializers.ValidationError('logo is not valid base64 image')
        return value

class FirmDetailSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add entity """
    uuid = serializers.CharField(max_length=1000, required=False, read_only=True)
    active = serializers.CharField(max_length=1000, required=False, read_only=True)
    date = serializers.CharField(max_length=1000, required=False, read_only=True)

    class Meta:
        """ attributs serialized """
        model = Firm
        fields = "__all__"
    
    def validate_social_raison(self, value):
        """ check validity of social_raison """
        try:
            f = Firm.objects.get(social_raison=value.upper())
            firm = self.context['firm']
            if f != firm:
                raise serializers.ValidationError('social_raison already exists')
            else:
                return value
        except Firm.DoesNotExist:
            return value

    def validate_niu(self, value):
        """ check validity of niu """
        try:
            f = Firm.objects.get(niu=value.upper())
            firm = self.context['firm']
            if f != firm:
                raise serializers.ValidationError('niu already exists')
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
                raise serializers.ValidationError('trade_register already exists')
            else:
                return value
        except Firm.DoesNotExist:
            return value
    
    def validate_type_person(self, value):
        """ check validity of type_person """
        if value not in [1,2,'1','2']:
            raise serializers.ValidationError('provide correct value for type_person')
        return value
    
    def validate_logo(self, value):
        """ check validity of logo """
        try:
            image = base64.b64decode(value)
            img = Image.open(io.BytesIO(image))
            if img.format.lower() in ACCEPT_IMAGE:
                width, height = img.size
                if width * height > MAX_IMAGE_SIZE:
                    raise serializers.ValidationError('image too large')
            else:
                raise serializers.ValidationError('not valid extension')
        except Exception:
            raise serializers.ValidationError('logo is not valid base64 image')
        return value