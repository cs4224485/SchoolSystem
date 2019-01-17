from school import models as scmodels
from rest_framework import serializers


class SchoolInfoSerialize(serializers.ModelSerializer):

    class Meta:
        model = scmodels.SchoolInfo
        fields = ['id', 'school_name', 'logo']
