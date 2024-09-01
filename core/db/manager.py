from . import fields as f
from typing import List
from core.utils.exceptions import ValidationError
from .defaults import DBDefaults


class ModelManager:

    TYPE = "type"
    FIELDS = "fields"
    DB_NAME = "db_name"

    def __init__(self, model) -> None:
        self.model = model()

    def _validate_fields(self, *args, **kwargs):
        """
        Check that only one field is allowed to have primary key
        if db doesn't have a primary key we can create a new auto generating primary key
        """
        db_name = kwargs.get(self.DB_NAME, None)
        if not db_name:
            raise ValidationError("Database name is not specified")
        self.model.db_name = db_name
        primary_key = 0
        field_objects = self._create_field_objects(*args, **kwargs)
        for field in field_objects:
            if field.primary_key:
                primary_key += 1
            if primary_key > 1:
                raise ValidationError(
                    f"Multiple primary key found in the database {db_name}"
                )
        if primary_key == 0:
            primary_key_field = f.StringField(
                name="__id",
                primary_key=True,
                max_length=34,
                default=DBDefaults.DEFAULT_ID,
            )
        fields = field_objects.copy()
        fields.append(primary_key_field)
        return fields

    def _create_field_objects(self, *args, **kwargs) -> List[f.Field]:
        fields = kwargs.get(self.FIELDS, [])
        field_objects = []
        for field in fields:
            field_type = field.get(self.TYPE, None)
            if field_type:
                # TODO: support so that list of validators names can be saved
                field_data = f.FieldMap[field_type].value()
                field_object = field_data.create(attrs=field)
                field_objects.append(field_object)
        return field_objects

    def _create(self, *args, **kwargs):
        return self._validate_fields(*args, **kwargs)

    def create(self, *args, **kwargs) -> None:
        """
        After validation I have to create these fields into pg database
        saving to db must be implemented in the Model class
        """
        fields = self._create(self, *args, **kwargs)
        self.model.fields = fields
        return self.model.save()
