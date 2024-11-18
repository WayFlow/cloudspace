from rest_framework.serializers import ModelSerializer

from company.models import ProjectLog

class ProjectLoggerSerializer(ModelSerializer):

    class Meta:
        model = ProjectLog
        fields = "__all__"

    def to_representation(self, project_log):
        return {"log": f"{project_log.level}: [{project_log.created_at}]: {project_log.log}"}