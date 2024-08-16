import uuid


class DBDefaults:

    DEFAULT_ID = "_call__default_id"

    """
    This class contains all the default functions.
    These fuctions can be called while saving data to the databse functions.
    Each function starts with the word default so that we can be differentiate it between
    other function such as validators

    each apis have a instance of this class
    """

    def _call__default_id(self):
        return str(uuid.uuid4())
