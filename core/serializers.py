from rest_framework.serializers import ModelSerializer

from company.models import ProjectLog

class ProjectLoggerSerializer(ModelSerializer):

    class Meta:
        model = ProjectLog
        fields = "__all__"