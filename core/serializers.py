from rest_framework.serializers import ModelSerializer

from company.models import ProjectLog

class ProjectLoggerSerializer(ModelSerializer):

    class Meta:
        model = ProjectLog
        fields = "__all__"

    def to_representation(self, instance : ProjectLog):
        repr = super().to_representation(instance)
        repr["project"] = str(instance.project.id)
        repr["env"] = str(instance.env.id)
        return repr
