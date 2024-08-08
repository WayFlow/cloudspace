class BaseModel(type):
    def __new__(cls, name, bases, dct):
        super_new = super().__new__
        return super_new()
    


