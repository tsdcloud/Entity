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
