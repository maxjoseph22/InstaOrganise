from lib.dog import Dog

'''
When I construct a dog
with the field
They are reflected in the instance properties
'''
def test_constructs_with_fields():
    dog = Dog(1, 'Poppy', 'Poodle', 4)
    assert dog.id == 1
    assert dog.name == "Poppy"
    assert dog.breed == "Poodle"
    assert dog.age == 4

'''
Test for Equality
'''
def test_equality_dog():
    dog_1 = Dog(1, 'Poppy', 'Poodle', 4)
    dog_2 = Dog(1, 'Poppy', 'Poodle', 4)
    assert dog_1 == dog_2

'''
Test for Formatting
'''
def test_formatting_dog():
    dog = Dog(1, 'Poppy', 'Poodle', 4)
    assert str(dog) == "Dog(1, Poppy, Poodle, 4)"