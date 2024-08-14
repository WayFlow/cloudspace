from collections import defaultdict
from typing import List

from pymongo import MongoClient

from company.models import Company, Project

"""

TODO: add django signals when ever any project is created or update in the
databse we need it to register in the MongoConnectionFactory and somehow
re-run the loading of mongo connections

"""


class MongoConnection:

    def __init__(self, connection_uri: str, db_name: str = None) -> None:
        self._connection_uri = connection_uri
        self._db_name = db_name
        self._client = None

    def connect(self) -> MongoClient:
        CONNECTION_STRING = f"{self._connection_uri}"
        client = MongoClient(CONNECTION_STRING, tz_aware=True)
        self._client = client if not self._db_name else client[self._db_name]

    @property
    def client(self):
        if not self._client:
            raise Exception(
                f"No client connection to MongoDB with connection uri: {self._connection_uri}. Have you called MongoConnection(...).connect()."
            )
        return self._client


class MongoConnectionFactory:

    _instance = None

    def __new__(cls) -> "MongoConnectionFactory":
        if not cls._instance:
            cls._instance = super(MongoConnectionFactory, cls).__new__(cls)
            cls._instance._connections_factory = defaultdict(MongoConnection)
        return cls._instance

    @classmethod
    def load_projects(cls):
        companies: List[Company] = Company.objects.all()
        for company in companies:
            company_id = company.id
            projects: List[Project] = company.get_company_projects.all()
            for project in projects:
                if project.mongo_connection_uri:
                    connection = MongoConnection(project.mongo_connection_uri)
                    try:
                        connection.connect()
                        cls._instance._connections_factory[
                            f"{company_id}_{project.id}"
                        ] = connection.client
                    except Exception as e:
                        print(e)
                else:
                    print(
                        f"No connection present for Company:{company.company_name} project:{project.project_name}."
                    )

    @classmethod
    def get_connection(cls, company_id, project_id):
        if not f"{company_id}_{project_id}" in cls._instance._connections_factory:
            raise Exception("No connection for give detaisl found in factory.")
        return cls._instance._connections_factory[f"{company_id}_{project_id}"]
