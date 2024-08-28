from enum import Enum

from core.utils import exceptions as exceptions
from core.utils import validators as validators
from .defaults import DBDefaults


class NOT_PROVIDED:
    pass


class Field:

    empty_values = list(validators.EMPTY_VALUES)

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
        help_text="",
        error_messages=None,
    ) -> None:
        self._name = name
        self._type = self.get_internal_type()
        self._primary_key = primary_key
        self._max_length = max_length
        self._unique = unique
        self._null = null
        self._db_index = db_index
        self._default = default
        self._serialize = serialize
        self._help_text = help_text
        self._validators = ()
        self._error_messages = error_messages

    def _check(self):
        return [
            *self._check_null_allowed_for_primary_key(),
            *self._check_validators(),
            *self._check_db_index(),
        ]

    def _check_db_index(self):
        if self._db_index not in (None, True, False):
            return [
                exceptions.ValidationError(
                    f"{self.__class__.__name__}.{self._name} 'db_index' must be None, True, or False"
                )
            ]
        return []

    def _check_validators(self):
        errors = []
        for _, validator in enumerate(self._validators):
            if not callable(validator):
                errors.append(
                    exceptions.ValidationError(
                        f"{self.__class__.__name__}.{self._name} all validators must be callable."
                    )
                )
        return errors

    def _check_null_allowed_for_primary_key(self):
        if not isinstance(self._primary_key, bool):
            return [
                exceptions.ValidationError(
                    f"{self.__class__.__name__}.{self._name} primary_key value Either True or False"
                )
            ]
        if self._null and self._primary_key:
            return [
                exceptions.ValidationError(
                    f"{self.__class__.__name__}.{self._name} for primary_key=True, null must be False",
                    code="null_allowed_for_primary_key",
                )
            ]
        return []

    def _is_default_callable(self):
        if (
            type(self._default) == str
            and len(self._default) > 7
            and self._default[:7] == "_call__"
        ):
            return True
        return False

    @property
    def _get_default(self):
        if self._is_default_callable():
            db_default = DBDefaults()
            attr = getattr(db_default, self._default)
            default_value = attr()
            return default_value
        return self._default

    def run_validator(self, value):
        """
        Only use it for saving a value in this field.
        """
        if value in self.empty_values:
            return
        errors = []
        for v in self._validators:
            try:
                v(value)
            except exceptions.ValidationError as e:
                if hasattr(e, "code") and e.code in self._error_messages:
                    e.message = self._error_messages[e.code]
                errors.extend(e.error_list)

        if errors:
            raise exceptions.ValidationError(errors)

    @property
    def unique(self):
        return self._unique | self._primary_key

    def get_internal_type(self):
        return self.__class__.__name__

    def to_python(self, value):
        return value

    def _create(self, *args, **kwargs):
        attrs = kwargs.pop("attrs", {})
        if attrs in validators.EMPTY_VALUES:
            raise exceptions.ValidationError(
                message=f"Empty field table property {self.__class__.__name__}",
                code="invalid_field",
            )
        for attr in attrs:
            cls_attr = hasattr(self, f"_{attr}")
            if cls_attr:
                setattr(self, f"_{attr}", attrs[attr])
            else:
                raise exceptions.ValidationError(
                    f"get unexprected keyword argument {attr} in {self.__class__.__name__} constructor"
                )
        errors = self._check()
        if errors:
            raise exceptions.ValidationError(errors)
        return self

    @property
    def primary_key(self):
        return self._primary_key

    def create(self, *args, **kwargs):
        return self._create(*args, **kwargs)


class BooleanField(Field):

    def to_python(self, value):
        if self._null and value in self._empty_values:
            return None
        if value in (True, False):
            # 1/0 are equal to True/False. bool() converts former to latter.
            return bool(value)
        if value in ("t", "True", "1"):
            return True
        if value in ("f", "False", "0"):
            return False
        raise exceptions.ValidationError(
            f"{self.__class__.__name__}.{self._name} Invalid boolean field value",
            code="invalid",
            params={"value": value},
        )

    def _check(self):
        errors = super()._check()
        if self._primary_key:
            errors.append(
                exceptions.ValidationError(
                    f"{self.__class__.__name__}.{self._name} boolean field cannot marked as primary key",
                )
            )
        if not isinstance(self._get_default, NOT_PROVIDED) and not isinstance(
            self._get_default, bool
        ):
            errors.append(
                exceptions.ValidationError(
                    f"{self.__class__.__name__}.{self._name} invalid default value: default value should either True or False",
                )
            )
        return errors


class StringField(Field):

    def to_python(self, value):
        if not isinstance(value, str):
            raise exceptions.ValidationError(
                f"{self.__class__.__name__}.{self._name} Invalid string field value",
                code="invalid",
                params={"value": value},
            )
        return value

    """
    Why I need to pass default in every field ?
    validations are not working properly 
    """

    def _check(self):
        errors = super()._check()
        if (
            not self._max_length
            or not isinstance(self._max_length, int)
            or self._max_length < 0
        ):
            errors.append(
                exceptions.ValidationError(
                    f"{self.__class__.__name__}.{self._name} max_length must be int and must not be -negative or zero"
                )
            )
        if not isinstance(self._get_default, NOT_PROVIDED) and not isinstance(
            self._get_default, str
        ):
            errors.append(
                exceptions.ValidationError(
                    f"{self.__class__.__name__}.{self._name} default value of the StringField must be a string"
                )
            )
        return errors


class TextField(Field):
    def to_python(self, value):
        if not isinstance(value, str):
            raise exceptions.ValidationError(
                f"{self.__class__.__name__}.{self._name} Invalid Text field value",
                code="invalid",
                params={"value": value},
            )
        return value

    def _check(self):
        errors = super()._check()
        if not isinstance(self._get_default, NOT_PROVIDED) and not isinstance(
            self._get_default, str
        ):
            errors.append(
                exceptions.ValidationError(
                    f"{self.__class__.__name__}.{self._name} default value of the TextField must be a string"
                )
            )
        return errors


class EmailField(Field): ...


class UrlField(Field): ...


class IntegerField(Field):

    def to_python(self, value):
        if not isinstance(value, int):
            raise exceptions.ValidationError(
                f"{self.__class__.__name__}.{self._name} Invalid string field value",
                code="invalid",
                params={"value": value},
            )
        return value

    def _check(self):
        errors = super()._check()
        if not isinstance(self._get_default, NOT_PROVIDED) and not isinstance(
            self._get_default, int
        ):
            errors.append(
                exceptions.ValidationError(
                    f"{self.__class__.__name__}.{self._name} default value of the StringField must be a string"
                )
            )
        return errors


class DecimalField(Field): ...


class DateField(Field): ...


class DateTimeField(Field): ...


class FieldMap(Enum):
    BooleanField = BooleanField
    StringField = StringField
    TextField = TextField
    EmailField = EmailField
    UrlField = UrlField
    IntegerField = IntegerField
    DecimalField = DecimalField
    DateField = DateField
    DateTimeField = DateTimeField
