# class Meta(type):
#     def __new__(cls, name, bases, dct):
#         super_new = super().__new__

#         parents = [b for b in bases]
#         print(parents)

#         return super().__new__(cls, name, bases, dct)


# class Person(metaclass=Meta):
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age

#     def greet(self):
#         return f"Hello, my name is {self.name} and I am {self.age} years old."


# p = Person("Alice", 30)

# class Animal(metaclass=Meta):
#     def __init__(self, species):
#         self.species = species

#     def speak(self):
#         return f"The {self.species} speaks!"


# a = Animal("Dog")


# class Living(Animal):
#     ...

# l = Living("aman")

# class A:
#     a = 5


# print(A.__dict__)
