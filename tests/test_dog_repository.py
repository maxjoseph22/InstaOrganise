from lib.dog_repository import *
from lib.dog import *

def test_get_all_dogs(db_connection): # See conftest.py to learn what `db_connection` is.
    db_connection.seed("seeds/dogs.sql") # Seed our database with some test data
    repository = DogRepository(db_connection) # Create a new DogRepository
    dogs = repository.all() # Get all dogs
    # Assert on the results
    assert dogs == [
        Dog(1, 'Benny', 'Poodle', 5),
        Dog(2, 'Spot', 'Labrador', 1),
        Dog(3, 'Honey', 'Lurcher', 10),
        Dog(4, 'Flea', 'Poodle', 2),
        Dog(5, 'Spot', 'Pitbull', 2)
    ]
    
def test_get_single_dog(db_connection):
    db_connection.seed("seeds/dogs.sql")
    repository = DogRepository(db_connection)
    dog = repository.find(3)
    assert dog == Dog(3, 'Honey', 'Lurcher', 10)

def test_get_dogs_by_name(db_connection):
    db_connection.seed("seeds/dogs.sql")
    repository = DogRepository(db_connection)
    dogs = repository.find_by_name('Honey')
    assert dogs == [Dog(3, 'Honey', 'Lurcher', 10)]

def test_get_dogs_by_name_with_multiple_results(db_connection):
    db_connection.seed("seeds/dogs.sql")
    repository = DogRepository(db_connection)
    dogs = repository.find_by_name('Spot')
    assert dogs == [Dog(2, 'Spot', 'Labrador', 1),
                    Dog(5, 'Spot', 'Pitbull', 2)]

def test_get_dogs_by_breed(db_connection):
    db_connection.seed("seeds/dogs.sql")
    repository = DogRepository(db_connection)
    dogs = repository.find_by_breed('Labrador')
    assert dogs == [Dog(2, 'Spot', 'Labrador', 1)]

def test_get_dogs_by_breed_with_multiple_results(db_connection):
    db_connection.seed("seeds/dogs.sql")
    repository = DogRepository(db_connection)
    dogs = repository.find_by_breed('Poodle')
    assert dogs == [
        Dog(1, 'Benny', 'Poodle', 5),
        Dog(4, 'Flea', 'Poodle', 2)
    ]

def test_get_dogs_by_age(db_connection):
    db_connection.seed("seeds/dogs.sql")
    repository = DogRepository(db_connection)
    dogs = repository.find_by_age(5)
    assert dogs == [Dog(1, 'Benny', 'Poodle', 5)]

def test_get_dogs_by_age_with_multiple_results(db_connection):
    db_connection.seed("seeds/dogs.sql")
    repository = DogRepository(db_connection)
    dogs = repository.find_by_age(2)
    assert dogs == [
        Dog(4, 'Flea', 'Poodle', 2),
        Dog(5, 'Spot', 'Pitbull', 2)
    ]

def test_create_dog(db_connection):
    db_connection.seed("seeds/dogs.sql")
    repository = DogRepository(db_connection)
    repository.create(Dog(None, 'Buddy', 'Great Dane', 3))
    dogs = repository.all()
    assert dogs == [
        Dog(1, 'Benny', 'Poodle', 5),
        Dog(2, 'Spot', 'Labrador', 1),
        Dog(3, 'Honey', 'Lurcher', 10),
        Dog(4, 'Flea', 'Poodle', 2),
        Dog(5, 'Spot', 'Pitbull', 2),
        Dog(6, 'Buddy', 'Great Dane', 3)
        
    ]

    
def test_delete_deletes_dog(db_connection):
    db_connection.seed("seeds/dogs.sql")
    repository = DogRepository(db_connection)
    repository.delete(3)
    dogs = repository.all()
    assert dogs == [
        Dog(1, 'Benny', 'Poodle', 5),
        Dog(2, 'Spot', 'Labrador', 1),
        Dog(4, 'Flea', 'Poodle', 2),
        Dog(5, 'Spot', 'Pitbull', 2)
    ]