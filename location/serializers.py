from rest_framework import serializers

from location.models import Country


class CountryStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add country """
    id = serializers.CharField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Country
        fields = [
            'name',
            'id'
        ]

    def validate_name(self, value):
        """ check validity of name """
        try:
            Country.objects.get(name=value.upper(), is_active=True)
            raise serializers.ValidationError(
                detail="name is already exists",
                code="already exists"
            )
        except Country.DoesNotExist:
            return value


class CountryDetailSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for update country """
    id = serializers.CharField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Country
        fields = [
            'name',
            'id'
        ]

    def validate_name(self, value):
        """ check validity of name """
        country = self.context['country']
        try:
            c = Country.objects.get(name=value.upper())
            if c != country:
                raise serializers.ValidationError(
                    detail="name is already exists",
                    code="already exists"
                )
            else:
                return value
        except Country.DoesNotExist:
            return value


class CountryDestroySerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for destroy country """
    id = serializers.CharField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Country
        fields = [
            'name',
            'id'
        ]

    def validate_name(self, value):
        """ check validity of name """
        country = self.context['country']
        regions = country.regions.filter(is_active=True)
        if len(regions) != 0:
            raise serializers.ValidationError(
                detail="regions already exists",
                code="regions already exists"
            )
        else:
            return value
