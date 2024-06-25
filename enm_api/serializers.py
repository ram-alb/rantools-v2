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
            r'^(((0)|([1-9]\d?)|(1\d\d)|(2[0-5]{2}))\.?){0,3}'
            r'((0)|([1-9]\d?)|(1\d\d)|(2[0-5]{2}))?$',
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


class ComandResultSerializer(serializers.Serializer):
    """Serializer for a ENM CLI command and its output."""

    command = serializers.CharField()
    output = serializers.CharField()

    def to_representation(self, instance):
        """Serialize a tuple of command result to a representation suitable for response."""
        return {
            'command': instance[0],
            'output': instance[1],
        }

    def to_internal_value(self, command_data):
        """Deserialize a command results to internal representation."""
        return (command_data['command'], command_data['output'])


class ObjectCreateResultSerializer(serializers.ListSerializer):
    """Serialize the results of commands executed during the creation of a Base Station object."""

    child = ComandResultSerializer()

    def to_representation(self, object_data):
        """Serialize a list of command results to a representation suitable for response."""
        return [self.child.to_representation(object_item) for object_item in object_data]

    def to_internal_value(self, object_data):
        """Deserialize a list of command results to internal representation."""
        return [self.child.to_internal_value(object_item) for object_item in object_data]


class EnmSerializer(serializers.Serializer):
    """Serializer for the ENM server."""

    enm = serializers.CharField()

    def validate_enm(self, enm):
        """Validate the ENM server identifier."""
        pattern = r'^ENM_SERVER_\d{1}$'
        if not re.match(pattern, enm):
            raise serializers.ValidationError(
                'Invalid ENM. Use one of ENM_SERVER_2 or ENM_SERVER_4',
            )
        return enm


class ControllersSerializer(serializers.Serializer):
    """Serializer for controllers information."""

    bsc = serializers.ListField(child=serializers.CharField())
    rnc = serializers.ListField(child=serializers.CharField())
