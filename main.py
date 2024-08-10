from core.db.fields import *

boolean_field = BooleanField()
try:
    created = boolean_field.create(attrs={
    "name": "is_active",
    "default": "ss",
    "db_index": "ss",
    "help_text": "If is active then it will shown in query",
})
    print(created)
except Exception as e:
    print(e.messages)