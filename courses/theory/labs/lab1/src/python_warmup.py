# Python is dynamically typed, which means that you don't specify variable types 
# in your declarations; the types are inferred at runtime
#
# define variable in Python
number = 10
list_ = [1, 2, 3, 4, 5]
dictionary = {
    "x": 10,
    "y": 20
}

# you can print variable by using build-int function `print()`
print(number)
print(list_)
print(dictionary)

# define function in Python
def add(x, y):
    return x + y

# you can add type of the parameter and return value by using type hint
# but the python will not check the type statically
def minus(x: int, y: int) -> int:
    return x - y


# call the functions we defined
print(add(10, 32))

# In Python, you can format you string by `f-string`
# In Python 3.12+, you can even call funciton inside `f-string`
print(f"52 - {number} = {minus(52, number)}")

# define class in Python
class Person:
    # you can think the `__init__()` funciton as constructor (Although it's not strictly true),
    # and add member variables for class here
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    # define method for class
    def say_hello(self):
        print(f"Hello, my name is {self.name}, I am {self.age} years old")


# In general, Python is a language that supports object-oriented thinking
class Student(Person):
    def __init__(self, name: str, age: int, id: str):
        super().__init__(name, age)
        self.id = id
    
    def say_hello(self):
        print(f"Hello, my name is {self.name}, My Student id is {self.id}")
        

# create instance of class
li  = Person("Ma Li", 30)
wang = Student("Lin Wang", 22, "SA23225000")

# use `for ... in ...` to iterate list
for people in [li, wang]:
    people.say_hello()
    
# use `if ... elif ... else ...` to make conditional judgments
for people in [li, wang]:
    if isinstance(people, Student):
        print(f"{people.name} is a student")
    elif isinstance(people, Person):
        print(f"{people.name} is a person")
    else:
        print(f"{people} is a unknown type")
        
    # in Python 3.12+, you can `match` to do the structural pattern matching
    # what will it output? Why？
    match people:
        case Person():
            print(f"{people.name} is a person")
        case Student():
            print(f"{people.name} is a student")
        case _:
            print(f"{people} is a unknown type")

# use `try ... expect ... finally ...` to do the exception handling
try:
    a = 1 / 0
except ZeroDivisionError:
    print("Find Division by zero error")
finally:
    print("It's always going to be executed!") 
