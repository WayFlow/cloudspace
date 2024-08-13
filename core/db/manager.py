from . import fields as f


class ModelManager:

    TYPE = "type"
    FIELDS = "fields"

    def __init__(self, **kwargs) -> None:
        self.kwargs = kwargs

    def create(self, *args, **kwargs) -> None:
        fields = kwargs.get(self.FIELDS, [])
        for field in fields:
            field_type = field.get(self.TYPE, None)
            if field_type:
                # TODO: add support for running default values as function
                #  add suppor so that list of validatos names can be saved
                # also validate that on model only creates one primary key
                created_field = f.FieldMap[field_type].value()
                print(created_field.create(attrs=field))
