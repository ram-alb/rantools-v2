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


class ObjectSerializer(serializers.Serializer):
    """Serializer of Base Station object parameters."""

    enm = serializers.CharField()
    subnetwork = serializers.CharField()
    sitename = serializers.CharField()
    platform = serializers.CharField()
    oam_ip = serializers.CharField()
    technologies = serializers.ListField(child=serializers.CharField())
    rnc = serializers.CharField(allow_null=True, required=False)
    bsc = serializers.CharField(allow_null=True, required=False)

    def validate_oam_ip(self, oam_ip):
        """Validate that the input is a valid IP address."""
        ip_regex = re.compile(
            r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$',
        )
        if not ip_regex.match(oam_ip):
            raise serializers.ValidationError("Invalid IP address format")
        return oam_ip

    def validate(self, object_data):
        """Validate `rnc` and `bsc` fields based on `technologies`."""
        technologies = object_data.get('technologies', [])
        rnc = object_data.get('rnc')
        bsc = object_data.get('bsc')

        if 'UMTS' in technologies and not rnc:
            raise serializers.ValidationError(
                {"rnc": "RNC is required if UMTS technology is present."},
            )

        if 'GSM' in technologies and not bsc:
            raise serializers.ValidationError(
                {"bsc": "BSC is required if GSM technology is present."},
            )

        return object_data


class ObjectInfoSerializer(serializers.Serializer):
    """Serializer for created Base Station object info."""

    object_info = serializers.ListField(child=serializers.CharField())
