from company.models import ProjectLog, Project
from utils import decorators

class Logger:

    @classmethod
    @decorators.background
    def error(cls, project : Project, log : str):
        try:
            ProjectLog.objects.create(project=project, log=log, level=ProjectLog.Level.ERROR)
        except Exception as e:
            print(str(e))

    @classmethod
    @decorators.background
    def info(cls, project, log):
        try:
            ProjectLog.objects.create(project=project, log=log, level=ProjectLog.Level.INFO)
        except Exception as e:
            print(str(e))

    @classmethod
    @decorators.background
    def warn(cls, project, log):
        try:
            ProjectLog.objects.create(project=project, log=log, level=ProjectLog.Level.WARN)
        except Exception as e:
            print(str(e))

    @classmethod
    def build_log(cls, project_log: ProjectLog) -> str:
        return f"{project_log.level}: [{project_log.created_at}:{project_log.log}]"