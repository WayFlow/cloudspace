from company.models import ProjectLog, Project
from core.serializers import ProjectLoggerSerializer
from utils import decorators
from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

import uuid

class Logger:

    @classmethod
    def _broadcast_log(cls, project_log : ProjectLog, env :str):
        channel_layer = get_channel_layer()
        project_log_group = f"{''.join(str(project_log.project.id).split('-'))}_{env}_logs"
        group_exists = async_to_sync(channel_layer.group_exists)(project_log_group)
        if group_exists:
            async_to_sync(channel_layer.group_send)(
                project_log_group,
                {
                    "type": "log",
                    "log": cls.build_log(project_log)
                }
            )

    @classmethod
    def save_log(cls, project :str, log :str, env: str, level: str):
        try:
            data={"project":project, "log":log, "level":level, "env":uuid.UUID(env)}
            serializer = ProjectLoggerSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            return serializer.save()
        except Exception as e:
            raise e
        

    @classmethod
    def log(cls, project : Project, log : str, env :str, level: str):
        if level == ProjectLog.Level.ERROR:
            cls._error(project, log, env)
        elif level == ProjectLog.Level.WARN:
            cls._warn(project, log, env)
        else:
            cls._info(project, log, env)


    @classmethod
    @decorators.background
    def _error(cls, project : Project, log : str, env :str):
        try:
            instance = cls.save_log(project.id, log, env, level=ProjectLog.Level.ERROR)
            cls._broadcast_log(instance, env)
        except Exception as e:
            print(str(e))

    @classmethod
    @decorators.background
    def _info(cls, project : Project, log : str, env :str):
        try:
            instance = cls.save_log(project.id, log, env, level=ProjectLog.Level.INFO)
            cls._broadcast_log(instance, env)
        except Exception as e:
            print(str(e))

    @classmethod
    @decorators.background
    def _warn(cls, project : Project, log : str, env :str):
        try:
            instance = cls.save_log(project.id, log, env, level=ProjectLog.Level.WARN)
            cls._broadcast_log(instance, env)
        except Exception as e:
            print(str(e))

    @classmethod
    def build_log(cls, project_log: ProjectLog) -> str:
        data = ProjectLoggerSerializer(project_log).data
        return data