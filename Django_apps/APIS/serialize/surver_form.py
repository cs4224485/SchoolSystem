from school.models import TableInfo
from rest_framework import serializers


class SchoolSerializers(serializers.ModelSerializer):
    class Meta:
        model = TableInfo
        fields = ['school_name', 'logo', 'address', 'province', 'city', 'region']




