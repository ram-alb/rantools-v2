import re

from rest_framework import serializers


class BscSerializer(serializers.Serializer):
    """Serializer for validating BSC names."""

    bsc = serializers.CharField()

    def validate_bsc(self, bsc_name):
        """Validate the format of the BSC name."""
        pattern = r'^[A-Z]{3,4}_[A-Z]\d{1,2}$'
        if not re.match(pattern, bsc_name):
            raise serializers.ValidationError("Invalid bsc_name")
        return bsc_name


class BscTgSerializer(serializers.Serializer):
    """Serializer for BSC TG data."""

    bsc = serializers.CharField()
    g12tg = serializers.ListField(child=serializers.IntegerField())
    g31tg = serializers.ListField(child=serializers.IntegerField())
