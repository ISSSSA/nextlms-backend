from rest_framework import serializers
from .models import XAPIStatement
import uuid
from dateutil.parser import parse

class XAPIStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = XAPIStatement
        fields = '__all__'
        read_only_fields = ('stored',)

    def validate_statement_id(self, value):
        try:
            uuid.UUID(str(value))
        except ValueError:
            raise serializers.ValidationError("statement_id must be a valid UUID")
        return value

    def validate_timestamp(self, value):
        if isinstance(value, str):
            try:
                return parse(value)
            except ValueError:
                raise serializers.ValidationError("Invalid timestamp format")
        return value

    def to_internal_value(self, data):
        if 'statement' not in data and all(field in data for field in ['actor', 'verb', 'object']):
            data = {'statement': data}

        return super().to_internal_value(data)