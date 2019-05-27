from rest_framework.viewsets import ViewSetMixin
from rest_framework.views import APIView
from school.models import TableSettings
from APIS.serialize.surver_form import SchoolSerializers


class FormReportViewSet(APIView):

    def get(self, request, *args, **kwargs):
        table_id = request.get('form_id')
        table_obj = TableSettings.objects.filter(id=table_id).first()
        school_obj = table_obj.school_range.all().first()
        school_se = SchoolSerializers(data=school_obj)


class StudentListViewSet(APIView):

    def get(self, request, *args, **kwargs):
        pass

