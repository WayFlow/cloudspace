from core.db import base

data = {
    "db_name": "test",
    "fields": [
        {
            "name": "id",
            "type": "StringField",
            "primary_key": True,
        },
        {
            "name": "name",
            "type": "StringField",
            "unique": True,
            "max_length": 30,
        },

    ]
}


try:
    base.Model.objects.create(**data)
except Exception as e:
    print(e.messages)