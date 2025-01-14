from lib.dog import Dog
import datetime

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
                row["link_to_post"], row["photo"]
            )
            dogs.append(item)
        return dogs
    
    # Retrieve breed popularity
    def get_breed_popularity(self):
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
            row["likes"], row["comments"], row["link_to_post"], row["photo"]
        )
    
    # Find dogs by name
    def find_by_name(self, name):
        rows = self._connection.execute('SELECT * FROM dogs WHERE name LIKE %s', [f'%{name}%'])
        dogs = []
        for row in rows:
            item = Dog(
                row["id"], row["name"], row["breed"], row["purebreed"], row["mix"],
                row["age"], row["sex"], row["location"], row["personality"],
                row["likes"], row["comments"], row["link_to_post"], row["photo"]
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
                row["likes"], row["comments"], row["link_to_post"], row["photo"]
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
                row["likes"], row["comments"], row["link_to_post"], row["photo"]
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
        """
        for dog in dogs
    )

        return readable_dogs
    
    # Create a new dog entry
    def create(self, dog):
        rows = self._connection.execute(
            '''
            INSERT INTO dogs (
                name, breed, purebreed, mix, age, sex, location, personality, 
                likes, comments, link_to_post, photo
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            ''', 
            [
                dog.name, dog.breed, bool(dog.purebreed), bool(dog.mix), int(dog.age), dog.sex,
                dog.location, dog.personality, dog.likes, dog.comments,
                dog.link_to_post, dog.photo
            ]
        )
        return rows[0]["id"]  # Return the generated ID
    
    # Delete a dog entry
    def delete(self, id):
        self._connection.execute('DELETE FROM dogs WHERE id = %s', [id])
        return None
