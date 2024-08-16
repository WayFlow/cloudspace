from typing import List

from . import manager
from .fields import Field


class Model:

    def __init__(self) -> None:
        self.db_name = None
        self.fields: List[Field] = []
        """
        Extra fields will created here based on the user design case.
        but for now I just have to create db_name and fields
        db_id in postgres
        """

    @classmethod
    def objects(cls):
        return manager.ModelManager(cls)

    def save(self, *args, **kwargs):
        fields = [field.__dict__ for field in self.fields]
        model = self.__dict__
        model["fields"] = fields
        return model
