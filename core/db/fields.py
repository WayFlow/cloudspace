class NOT_PROVIDED:
    pass


class Field:

    def __init__(
            self, 
            name=None,
            primary_key=False,
            max_length=None,
            unique=False,
            null=False,
            db_index=False,
            default=NOT_PROVIDED,
            serialize=True,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            choices=None,
            help_text="",
            validators=(),
            error_messages=None,
        ) -> None:
        self.name = name
        self.primary_key = primary_key
        self.max_length = max_length
        self.unique = unique
        self.null = null
        self.db_index = db_index
        self.default = default
        self.serialize = serialize
        self.unique_for_date = unique_for_date
        self.unique_for_month = unique_for_month
        self.unique_for_year = unique_for_year
        self.choices = choices
        self.help_text = help_text
        self.validators = validators
        self.error_messages = error_messages
    
    

    def save(self, *args, **kwargs):
        
        ...



class BooleanField(Field):
    ...


class StringField(Field):
    ...


class TextField(Field):
    ...

# TODO: add support for mixins for auto default time and date
class DateField(Field):
    ...

class DateTimeField(Field):
    ...

class IntegerField(Field):
    ...

class DecimalField(Field):
    ...

class EmailField(Field):
    ...


class UrlField(Field):
    ...