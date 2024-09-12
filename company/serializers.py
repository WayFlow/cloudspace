from rest_framework.serializers import ModelSerializer
from .models import Company, Project, ProjectEnvironment


class CompanySerializer(ModelSerializer):

    class Meta:
        model = Company
        fields = "__all__"


class ProjectSerializer(ModelSerializer):
    # TODO: handle project secret_key visibility

    class Meta:
        model = Project
        fields = "__all__"

    def to_representation(self, instance: Project):
        repr = super().to_representation(instance)
        repr["company"] = CompanySerializer(instance.company).data
        return repr


class ProjectEnvironmentSerializer(ModelSerializer):

    class Meta:
        model = ProjectEnvironment
        fields = "__all__"

    def to_representation(self, instance: ProjectEnvironment):
        repr = super().to_representation(instance)
        repr["project"] = CompanySerializer(instance.project).data
        return repr
