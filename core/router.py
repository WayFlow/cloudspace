import uuid

from typing import List

from rest_framework.permissions import AllowAny
from rest_framework.urls import path

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import *

from company.models import *
from core.urls import urlpatterns
from core.loggers import Logger


'''

Chain of responsibity Pattern

'''

class AbstractAPIRegistrationHandler:

    @classmethod
    def handle(cls):
        return GetAPIForRegistrationFromDB.next()
    
    @classmethod
    def register(cls, api: API):
        return CreateAPIEnpoint.next(api)



class GetAPIForRegistrationFromDB(AbstractAPIRegistrationHandler):

    @classmethod
    def _load_apis(cls):
        return API.objects.all()

    @classmethod
    def next(cls):
        return BuildAPIEnpointFlow.next(cls._load_apis())
    

class BuildAPIEnpointFlow(AbstractAPIRegistrationHandler):
    
    @classmethod
    def next(cls, apis: List[API]):
        for api in apis:
            CreateAPIEnpoint.next(api)


class CreateAPIEnpoint(AbstractAPIRegistrationHandler):

    @classmethod
    def build_flow(cls, api: API):
        return APIFlowBuilder(api)

    @classmethod
    def next(cls, api: API):
        endpoint_prefix = api.project.company.route
        endpoint_path = api.endpoint
        name = api.name
        handler = cls.build_flow(api).handler_class
        route = f"{endpoint_prefix}/{endpoint_path}"
        urlpattern = path(route, handler, name=name)
        urlpatterns.append(urlpattern)
        
class APIFlowBuilder(AbstractAPIRegistrationHandler):


    def __init__(self, api : API):
        super().__init__()
        self.api = api

    

    def _authentication(self):
        '''
        TODO: for now all apis are not authenticated need to a 
        authentication method to be implemented for the apis
        '''
        return AllowAny
    
    def _get(self):
        @api_view(["GET"])
        @permission_classes([AllowAny])
        def handler(request, **kwargs):
            return self._build_api_body(request, **kwargs)
        return handler

    
    def _post(self):
        @api_view(["POST"])
        @permission_classes([AllowAny])
        def handler(request, **kwargs):
            return self._build_api_body(request, **kwargs)
        return handler

    def _put(self):   
        @api_view(["PUT"])
        @permission_classes([AllowAny])
        def handler(request, **kwargs):
            return self._build_api_body(request, **kwargs)
        return handler


    def _delete(self):
        @api_view(["DELETE"])
        @permission_classes([AllowAny])
        def handler(request, **kwargs):
            return self._build_api_body(request, **kwargs)
        return handler


    def _handle_api_method(self):
        handler_method_name = f"_{self.api.method.lower()}"
        handler_method = getattr(self, handler_method_name)
        return handler_method



    def _build_api_body(self, request, **kwargs):
        return LoadAPIBodyFromNeo(self.api).build(request, **kwargs)

    @property
    def handler_class(self):
        view = self._handle_api_method()
        return view()


class LoadAPIBodyFromNeo(AbstractAPIRegistrationHandler):

    def __init__(self, api: API):
        super().__init__()
        self.api = api

    # TODO: make decorator with this so that we can directly apply to build function
    def _log_api_call(self, request, status_code, **kwargs):
        if status_code >= 100 and status_code < 400:
            Logger.log(self.api.project, f"{self.api.method} '{request.path}' {status_code}", env=request.headers.get("Env-Id"), level=ProjectLog.Level.INFO)
        elif status_code == 404:
            Logger.log(self.api.project, f"{self.api.method} '{request.path}' 404", env=request.headers.get("Env-Id"), level=ProjectLog.Level.WARN)
        else:
            Logger.log(self.api.project, f"{self.api.method} '{request.path}' {status_code}", env=request.headers.get("Env-Id"), level=ProjectLog.Level.ERROR)

    def _check_requester_authenticity(self, request) -> {bool, str}:
        try:
            envId = request.headers.get('Env-Id')
            projectId = request.headers.get('Project-Id')
            if envId is None or projectId is None:
                return False, "missing Env-Id or Project-Id in headers"
            if self.api.project.id != uuid.UUID(projectId):
                return False, "api is not associated with the provided projectId"
            env = Environment.objects.filter(id=envId, company=self.api.project.company).first()
            if not env:
                return False, "envId is not associated with projectId"
            return True, ""
        except:
            return False, "Invalid Project-Id or Env-Id in headers"
    
    # find a better way to do it
    def build(self, request, **kwargs):
        authentic, message = self._check_requester_authenticity(request)
        if not authentic:
            self._log_api_call(request, HTTP_403_FORBIDDEN)
            return Response(message, status=HTTP_403_FORBIDDEN)
        self._log_api_call(request, HTTP_204_NO_CONTENT)
        return Response(status=HTTP_204_NO_CONTENT)