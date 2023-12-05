from rest_framework import serializers

from location.models import (
    Country,
    Region,
    Department,
    Municipality,
    Village,
    Location,
    Firm
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
    name = serializers.CharField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Country
        fields = [
            'name',
            'id',
            'is_active'
        ]

    def validate(self, value):
        """ check validity """
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
    country = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Region
        fields = [
            'name',
            'id',
            'country_id',
            'country'
        ]

    def get_country(self, instance):
        data = {
            "id": instance.country.id,
            "name": instance.country.name
        }
        return data

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
            Region.objects.get(
                country=country,
                name=data['name'].upper(),
                is_active=True
            )
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
    country = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Region
        fields = [
            'name',
            'id',
            'is_active',
            'country'
        ]

    def get_country(self, instance):
        data = {
            "id": instance.country.id,
            "name": instance.country.name
        }
        return data

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
    name = serializers.CharField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Region
        fields = [
            'name',
            'id',
            'is_active'
        ]

    def validate(self, value):
        """ check validity """
        region = self.context['region']
        departments = region.departments.filter(is_active=True)
        if len(departments) != 0:
            raise serializers.ValidationError(
                detail="departments already exists",
                code="departments already exists"
            )
        else:
            return value


class DepartmentStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add department """
    id = serializers.CharField(read_only=True)
    region_id = serializers.CharField(write_only=True)
    region = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Department
        fields = [
            'name',
            'id',
            'region_id',
            'region'
        ]

    def get_region(self, instance):
        return {
            "id": instance.region.id,
            "name": instance.region.name
        }

    def validate_region_id(self, value):
        """ check validity of region_id """
        try:
            Region.objects.get(id=value, is_active=True)
        except Region.DoesNotExist:
            raise serializers.ValidationError(
                detail="region not found",
                code="not found"
            )
        return value

    def validate(self, data):
        """ check validity """
        region = Region.objects.get(
            id=data['region_id'], is_active=True)
        try:
            Department.objects.get(
                region=region,
                name=data['name'].upper(),
                is_active=True
            )
            raise serializers.ValidationError(
                detail="name is already exists",
                code="already exists"
            )
        except Department.DoesNotExist:
            return data


class DepartementDetailSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for update department """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Department
        fields = [
            'name',
            'id',
            'is_active'
        ]

    def validate(self, data):
        """ check validity """
        department = self.context['department']
        try:
            d = Department.objects.get(
                name=data['name'].upper(),
                region=department.region
            )
            if d != department:
                raise serializers.ValidationError(
                    detail="name is already exists",
                    code="already exists"
                )
        except Department.DoesNotExist:
            pass
        return data


class DepartmentDestroySerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for destroy department """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Department
        fields = [
            'name',
            'id',
            'is_active'
        ]

    def validate(self, value):
        """ check validity """
        department = self.context['department']
        municipaliies = department.municipalities.filter(is_active=True)
        if len(municipaliies) != 0:
            raise serializers.ValidationError(
                detail="municipality already exists",
                code="municipality already exists"
            )
        else:
            return value


class MunicipalityStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add municipality """
    id = serializers.CharField(read_only=True)
    department_id = serializers.CharField(write_only=True)
    department = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Municipality
        fields = [
            'name',
            'id',
            'department_id',
            'department'
        ]

    def get_department(self, instance):
        return {
            "id": instance.department.id,
            "name": instance.department.name
        }

    def validate_department_id(self, value):
        """ check validity of department_id """
        try:
            Department.objects.get(id=value, is_active=True)
        except Department.DoesNotExist:
            raise serializers.ValidationError(
                detail="department not found",
                code="not found"
            )
        return value

    def validate(self, data):
        """ check validity """
        department = Department.objects.get(
            id=data['department_id'], is_active=True)
        try:
            Municipality.objects.get(
                department=department,
                name=data['name'].upper(),
                is_active=True
            )
            raise serializers.ValidationError(
                detail="name is already exists",
                code="already exists"
            )
        except Municipality.DoesNotExist:
            return data


class MunicipalityDetailSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for update municipality """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Municipality
        fields = [
            'name',
            'id',
            'is_active'
        ]

    def validate(self, data):
        """ check validity """
        municipality = self.context['municipality']
        try:
            m = Municipality.objects.get(
                name=data['name'].upper(),
                department=municipality.department
            )
            if m != municipality:
                raise serializers.ValidationError(
                    detail="name is already exists",
                    code="already exists"
                )
        except Municipality.DoesNotExist:
            pass
        return data


class MunicipalityDestroySerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for destroy municipality """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Municipality
        fields = [
            'name',
            'id',
            'is_active'
        ]

    def validate(self, value):
        """ check validity """
        municipality = self.context['municipality']
        villages = municipality.villages.filter(is_active=True)
        if len(villages) != 0:
            raise serializers.ValidationError(
                detail="villages already exists",
                code="villages already exists"
            )
        else:
            return value


class VillageStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add village """
    id = serializers.CharField(read_only=True)
    municipality_id = serializers.CharField(write_only=True)
    municipality = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Village
        fields = [
            'name',
            'id',
            'municipality_id',
            'municipality'
        ]

    def get_municipality(self, instance):
        return {
            "id": instance.municipality.id,
            "name": instance.municipality.name
        }

    def validate_municipality_id(self, value):
        """ check validity of municipality_id """
        try:
            Municipality.objects.get(id=value, is_active=True)
        except Municipality.DoesNotExist:
            raise serializers.ValidationError(
                detail="municipality not found",
                code="not found"
            )
        return value

    def validate(self, data):
        """ check validity """
        municipality = Municipality.objects.get(
            id=data['municipality_id'], is_active=True)
        try:
            Village.objects.get(
                municipality=municipality,
                name=data['name'].upper(),
                is_active=True
            )
            raise serializers.ValidationError(
                detail="name is already exists",
                code="already exists"
            )
        except Village.DoesNotExist:
            return data


class VillageDetailSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for update village """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Village
        fields = [
            'name',
            'id',
            'is_active'
        ]

    def validate(self, data):
        """ check validity """
        village = self.context['village']
        try:
            v = Village.objects.get(
                name=data['name'].upper(),
                municipality=village.municipality
            )
            if v != village:
                raise serializers.ValidationError(
                    detail="name is already exists",
                    code="already exists"
                )
        except Village.DoesNotExist:
            pass
        return data


class VillageDestroySerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for destroy village """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Village
        fields = [
            'name',
            'id',
            'is_active'
        ]

    def validate(self, value):
        """ check validity of name """
        village = self.context['village']
        locations = village.locations.filter(is_active=True)
        if len(locations) != 0:
            raise serializers.ValidationError(
                detail="locations already exists",
                code="locations already exists"
            )
        else:
            return value


class LocationStoreSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for add location """
    id = serializers.CharField(read_only=True)
    village_id = serializers.CharField(write_only=True)
    firm_id = serializers.CharField(write_only=True)
    firm = serializers.SerializerMethodField(read_only=True)
    village = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Location
        fields = [
            'name',
            'id',
            'village_id',
            'firm_id',
            'firm',
            'village'
        ]

    def get_firm(self, instance):
        return {
            "id": instance.firm.id,
            "business_name": instance.firm.business_name,
            "acronym": instance.firm.acronym,
            "logo": instance.firm.logo
        }

    def get_village(self, instance):
        return {
            "id": instance.village.id,
            "name": instance.village.name
        }

    def validate_village_id(self, value):
        """ check validity of village_id """
        try:
            Village.objects.get(id=value, is_active=True)
        except Village.DoesNotExist:
            raise serializers.ValidationError(
                detail="village not found",
                code="not found"
            )
        return value

    def validate_firm_id(self, value):
        """ check validity of firm_id """
        try:
            Firm.objects.get(id=value, is_active=True)
        except Firm.DoesNotExist:
            raise serializers.ValidationError(
                detail="firm not found",
                code="not found"
            )
        return value

    def validate(self, data):
        """ check validity """
        village = Village.objects.get(
            id=data['village_id'])
        firm = Firm.objects.get(
            id=data['firm_id']
        )
        try:
            Location.objects.get(
                firm=firm,
                village=village,
                name=data['name'].upper(),
                is_active=True
            )
            raise serializers.ValidationError(
                detail="name is already exists",
                code="already exists"
            )
        except Location.DoesNotExist:
            return data


class LocationDetailSerializer(serializers.HyperlinkedModelSerializer):
    """ logical validataion for update location """
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    firm = serializers.SerializerMethodField(read_only=True)
    village = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """ attributs serialized """
        model = Location
        fields = [
            'name',
            'id',
            'is_active',
            'firm',
            'village'
        ]

    def get_firm(self, instance):
        return {
            "id": instance.firm.id,
            "business_name": instance.firm.business_name,
            "acronym": instance.firm.acronym,
            "logo": instance.firm.logo
        }

    def get_village(self, instance):
        return {
            "id": instance.village.id,
            "name": instance.village.name
        }

    def validate(self, data):
        """ check validity """
        location = self.context['location']
        try:
            lo = Location.objects.get(
                name=data['name'].upper(),
                village=location.village,
                firm=location.firm
            )
            if lo != location:
                raise serializers.ValidationError(
                    detail="name is already exists",
                    code="already exists"
                )
        except Location.DoesNotExist:
            pass
        return data
