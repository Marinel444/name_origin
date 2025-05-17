from rest_framework import serializers
from .models import Country, Name


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class NameSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = Name
        fields = ("name", "probability", "request_count", "last_accessed_at", "country")
