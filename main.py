# from core.db import base
# from core.utils import exceptions

# data = {
#     "db_name": "test_db",
#     "fields": [
#         {
#             "name": "address",
#             "type": "TextField",
#             "default": "some"
#         },
#         {
#             "name": "name",
#             "type": "StringField",
#             "unique": True,
#             "max_length": 30,
#             "default": "name",
#         },
#     ],
# }


# try:
#     test_db = base.Model.objects().create(**data)
#     print(test_db)
# except exceptions.ValidationError as e:
#     print(e.messages)
# except Exception as e:
#     print(e)

from tokens.token import *

acc = Account.objects.all().first()

refresh = RefreshToken(acc).create()
access = AccessToken(acc).create()
