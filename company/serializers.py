from rest_framework.serializers import ModelSerializer
from .models import Company, Project, Environment


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


class EnvironmentSerializer(ModelSerializer):

    class Meta:
        model = Environment
        fields = "__all__"
