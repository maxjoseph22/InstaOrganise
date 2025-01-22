from lib.dog import Dog
import datetime
from colorama import init, Fore, Style
import random

class DogRepository:
    # Initialize with a database connection
    def __init__(self, connection):
        self._connection = connection

    # Retrieve all dogs
    def all(self):
        rows = self._connection.execute('SELECT * FROM dogs')
        dogs = []
        for row in rows:
            item = Dog(
                row["id"], row["name"], row["breed"], row["purebreed"],
                row["mix"], row["age"], row["sex"], row["location"],
                row["personality"], row["likes"], row["comments"],
                row["link_to_post"], row["photo"], row["breed_id"]
            )
            dogs.append(item)
        return dogs
    
    # Retrieve breed popularity
    def get_breed_popularity(self):
        rows = self._connection.execute(
            'SELECT name, COUNT(*) AS count FROM dogs GROUP BY name ORDER BY likes DESC'
        )
        result = []
        for row in rows:
            result.append(f"{row['name']}, {row['count']}")
        return result
    
    # Retrieve popularity by likes
    def get_likes_popularity(self):
        rows = self._connection.execute(
            'SELECT breed, COUNT(*) AS count FROM dogs GROUP BY breed ORDER BY count DESC'
        )
        result = []
        for row in rows:
            result.append(f"{row['breed']}, {row['count']}")
        return result
    
    # Retrieve name popularity
    def get_name_popularity(self):
        rows = self._connection.execute(
            'SELECT name, COUNT(*) AS count FROM dogs GROUP BY name ORDER BY count DESC'
        )
        result = []
        for row in rows:
            result.append(f"{row['name']}, {row['count']}")
        return result
    
    # Find a dog by ID
    def find(self, id):
        rows = self._connection.execute('SELECT * FROM dogs WHERE id = %s', [id])
        row = rows[0]
        return Dog(
            row["id"], row["name"], row["breed"], row["purebreed"], row["mix"],
            row["age"], row["sex"], row["location"], row["personality"],
            row["likes"], row["comments"], row["link_to_post"], row["photo"], row["breed_id"]
        )
    
    # Find dogs by name
    def find_by_name(self, name):
        rows = self._connection.execute('SELECT * FROM dogs WHERE name LIKE %s', [f'%{name}%'])
        dogs = []
        for row in rows:
            item = Dog(
                row["id"], row["name"], row["breed"], row["purebreed"], row["mix"],
                row["age"], row["sex"], row["location"], row["personality"],
                row["likes"], row["comments"], row["link_to_post"], row["photo"], row["breed_id"]
            )
            dogs.append(item)
        
        readable_dogs = "\n\n".join(
        f"""
        ID: {dog.id}
        Name: {dog.name}
        Breed: {dog.breed}
        Purebred: {"Yes" if dog.purebreed else "No"}
        Mix: {dog.mix}
        Age: {dog.age}
        Sex: {dog.sex}
        Location: {dog.location}
        Personality: {dog.personality}
        Likes: {dog.likes}
        Comments: {dog.comments}
        Link to Post: {dog.link_to_post}
        Photo URL: {dog.photo}
        Breed ID: {dog.breed_id}
        """
        for dog in dogs
    )

        return readable_dogs
        
        
    # Find dogs by breed
    def find_by_breed(self, breed):
        rows = self._connection.execute('SELECT * FROM dogs WHERE breed LIKE %s', [f'%{breed}%'])
        dogs = []
        for row in rows:
            item = Dog(
                row["id"], row["name"], row["breed"], row["purebreed"], row["mix"],
                row["age"], row["sex"], row["location"], row["personality"],
                row["likes"], row["comments"], row["link_to_post"], row["photo"], row["breed_id"]
            )
            dogs.append(item)
        
        readable_dogs = "\n\n".join(
        f"""
        ID: {dog.id}
        Name: {dog.name}
        Breed: {dog.breed}
        Purebred: {"Yes" if dog.purebreed else "No"}
        Mix: {dog.mix}
        Age: {dog.age}
        Sex: {dog.sex}
        Location: {dog.location}
        Personality: {dog.personality}
        Likes: {dog.likes}
        Comments: {dog.comments}
        Link to Post: {dog.link_to_post}
        Photo URL: {dog.photo}
        Breed ID: {dog.breed_id}
        """
        for dog in dogs
    )
        return readable_dogs
    
    # Find dogs by age
    def find_by_age(self, age):
        rows = self._connection.execute('SELECT * FROM dogs WHERE age LIKE %s', [f'%{age}%'])
        dogs = []
        for row in rows:
            item = Dog(
                row["id"], row["name"], row["breed"], row["purebreed"], row["mix"],
                row["age"], row["sex"], row["location"], row["personality"],
                row["likes"], row["comments"], row["link_to_post"], row["photo"], row["breed_id"]
            )
            dogs.append(item)
        
        readable_dogs = "\n\n".join(
        f"""
        ID: {dog.id}
        Name: {dog.name}
        Breed: {dog.breed}
        Purebred: {"Yes" if dog.purebreed else "No"}
        Mix: {dog.mix}
        Age: {dog.age}
        Sex: {dog.sex}
        Location: {dog.location}
        Personality: {dog.personality}
        Likes: {dog.likes}
        Comments: {dog.comments}
        Link to Post: {dog.link_to_post}
        Photo URL: {dog.photo}
        Breed ID: {dog.breed_id}
        """
        for dog in dogs
    )

        return readable_dogs
    
    # Create a new dog entry
    def create(self, dog):
        # First try to find the breed in the purebred table
        breed_rows = self._connection.execute(
            'SELECT id FROM breeds WHERE breed_name = %s',
            [dog.breed]
        )

        # If found in purebred table, use that ID and set purebreed=True
        if len(breed_rows) > 0:
            breed_id = breed_rows[0]["id"]
            rows = self._connection.execute(
                '''
                INSERT INTO dogs (
                    name, breed, purebreed, mix, age, sex, location, personality, 
                    likes, comments, link_to_post, photo, breed_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                ''', 
                [
                    dog.name, dog.breed, True, False, dog.age, dog.sex,
                    dog.location, dog.personality, dog.likes, dog.comments,
                    dog.link_to_post, dog.photo, breed_id
                ]
            )
        # If not found in purebred table, check cross breeds table
        else:
            cross_breed_rows = self._connection.execute(
                'SELECT id FROM cross_breeds WHERE breed_name = %s',
                [dog.breed]
            )

            if len(cross_breed_rows) == 0:
                raise ValueError(f"Breed '{dog.breed}' not found in either breeds or cross breeds tables")

            cross_breed_id = cross_breed_rows[0]["id"]
            rows = self._connection.execute(
                '''
                INSERT INTO dogs (
                    name, breed, purebreed, mix, age, sex, location, personality, 
                    likes, comments, link_to_post, photo, cross_breed_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                ''', 
                [
                    dog.name, dog.breed, False, True, dog.age, dog.sex,
                    dog.location, dog.personality, dog.likes, dog.comments,
                    dog.link_to_post, dog.photo, cross_breed_id
                ]
            )

        return rows[0]["id"]
    
    # Get random dog
    def random_dog(self):
        range_list = self._connection.execute('SELECT COUNT(*) FROM dogs')
        range_dict = range_list[0]
        range_num = range_dict['count']
        random_num = random.randrange(1, range_num)

        rows = self._connection.execute('SELECT * FROM dogs WHERE id = %s', [random_num])
        dogs = []
        for row in rows:
            item = Dog(
                row["id"], row["name"], row["breed"], row["purebreed"], row["mix"],
                row["age"], row["sex"], row["location"], row["personality"],
                row["likes"], row["comments"], row["link_to_post"], row["photo"], row["breed_id"], row["cross_breed_id"]
            )
            dogs.append(item)
        
        readable_dogs = "\n\n".join(
        f"""
        ID: {dog.id}
        Name: {dog.name}
        Breed: {dog.breed}
        Purebred: {"Yes" if dog.purebreed else "No"}
        Mix: {dog.mix}
        Age: {dog.age}
        Sex: {dog.sex}
        Location: {dog.location}
        Personality: {dog.personality}
        Likes: {dog.likes}
        Comments: {dog.comments}
        Link to Post: {dog.link_to_post}
        Photo URL: {dog.photo}
        Breed ID: {dog.breed_id}
        Cross breed ID: {dog.cross_breed_id}
        """
        for dog in dogs
    )
        return readable_dogs

    # Delete a dog entry
    def delete(self, id):
        self._connection.execute('DELETE FROM dogs WHERE id = %s', [id])
        return None
