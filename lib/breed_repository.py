from lib.breed import Breed
import datetime

class BreedRepository:

    def __init__(self, connection):
        self._connection = connection

    # Retrieve all breeds
    def all(self):
        rows = self._connection.execute('SELECT * FROM breeds')
        breeds = []
        for row in rows:
            item = Breed(
                row["id"], row["breed_name"], row["count"]
            )
            breeds.append(item)
        return breeds
    
    # Retrieve breed popularity
    def get_breed_popularity(self):
        rows = self._connection.execute(
            'SELECT breed_name, count FROM breeds ORDER BY count DESC'
        )
        return [f"{row['breed_name']}, {row['count']}" for row in rows]
        
    # Find dogs by breed

    def find_by_specific_breed(self, breed_name):
        rows = self._connection.execute('SELECT * FROM breeds WHERE breed_name = %s', [breed_name])
        if not rows:  # Handle case where no rows are returned
            return "Breed not found"
        row = rows[0]
        return Breed(
                row["id"], row["breed_name"], row["count"]
            )
    
    def find_by_general_breed(self, breed_name):
        rows = self._connection.execute('SELECT * FROM breeds WHERE breed_name LIKE %s', [f'%{breed_name}%'])
        breeds = []
        for row in rows:
            item = Breed(
                row["id"], row["breed_name"], row["count"]
            )
            breeds.append(item)
        return breeds
    
    # Find breed and add to count
    def find_by_breed_and_add_to_count(self, breed_name):
        result = self._connection.execute('UPDATE breeds SET count = count + 1 WHERE breed_name = %s', [breed_name])
        if result.rowcount > 0:
            return f"Successfully increased count for breed '{breed_name}'."
        else:
            return f"No breed found with the name {breed_name}."

    # Delete a breed entry
    def delete(self, id):
        self._connection.execute('DELETE FROM breeds WHERE id = %s', [id])
        return None
