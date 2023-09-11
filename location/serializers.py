from rest_framework import serializers

from location.models import (
    Country,
    Region
)


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
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Country
        fields = [
            'name',
            'id',
            'is_active'
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
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Country
        fields = [
            'name',
            'id',
            'is_active'
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


class RegionStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add region """
    id = serializers.CharField(read_only=True)
    country_id = serializers.CharField(write_only=True)

    class Meta:
        """ attributs serialized """
        model = Region
        fields = [
            'name',
            'id',
            'country_id'
        ]

    def validate_country_id(self, value):
        """ check validity of country """
        try:
            Country.objects.get(id=value, is_active=True)
        except Country.DoesNotExist:
            raise serializers.ValidationError(
                detail="country not found",
                code="not found"
            )
        return value

    def validate(self, data):
        """ check validity """
        country = Country.objects.get(
            id=data['country_id'], is_active=True)
        try:
            Region.objects.get(country=country, name=data['name'])
            raise serializers.ValidationError(
                detail="name is already exists",
                code="already exists"
            )
        except Region.DoesNotExist:
            return data


class RegionDetailSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for update region """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Country
        fields = [
            'name',
            'id',
            'is_active'
        ]

    def validate(self, data):
        """ check validity """
        region = self.context['region']
        try:
            r = Region.objects.get(
                name=data['name'].upper(),
                country=region.country
            )
            if r != region:
                raise serializers.ValidationError(
                    detail="name is already exists",
                    code="already exists"
                )
        except Region.DoesNotExist:
            pass
        return data


class RegionDestroySerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for destroy country """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Country
        fields = [
            'name',
            'id',
            'is_active'
        ]

    def validate_name(self, value):
        """ check validity of name """
        region = self.context['region']
        departments = region.departments.filter(is_active=True)
        if len(departments) != 0:
            raise serializers.ValidationError(
                detail="departments already exists",
                code="departments already exists"
            )
        else:
            return value
