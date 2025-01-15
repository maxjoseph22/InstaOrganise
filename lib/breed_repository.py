from lib.breed import Breed
import datetime
from colorama import init, Fore, Style

class BreedRepository:

    def __init__(self, connection):
        self._connection = connection

    # Retrieve all breeds
    def all(self):
        rows = self._connection.execute('SELECT * FROM breeds')
        all_breeds = []
        for row in rows:
            item = Breed(
                row["id"], row["breed_name"], row["count"]
            )
            all_breeds.append(item)
        return all_breeds
    
    def get_breed_alphabetically(self):
        rows = self._connection.execute(
            'SELECT breed_name, count FROM breeds ORDER BY breed_name ASC'
        )
        return [f"{row['breed_name']}, {row['count']}" for row in rows]
    
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
        cross_breed_rows = self._connection.execute(
        'SELECT * FROM cross_breeds WHERE breed_name = %s', 
        [breed_name]
        )

        if len(cross_breed_rows) > 0:  # If found in cross_breeds
            self._connection.execute(
                'UPDATE cross_breeds SET count = count + 1 WHERE breed_name = %s', 
                [breed_name]
            )
            return f"{Fore.GREEN}Cross breed count successfully updated{Style.RESET_ALL}"

        rows = self._connection.execute('SELECT * FROM breeds WHERE breed_name = %s', [breed_name])
        if not rows:  # Handle case where no rows are returned
            self._connection.execute('INSERT INTO cross_breeds (breed_name, count) VALUES (%s, 1)', [breed_name])
            return f"{Fore.YELLOW}Breed not found. Added to cross breeds table.{Style.RESET_ALL}"
        else:
            self._connection.execute(
        'UPDATE breeds SET count = count + 1 WHERE breed_name = %s', 
        [breed_name]
        )
            return f"{Fore.GREEN}Breed count successfully updated{Style.RESET_ALL}"

    # Retrieve all breeds with zero count i.e. never seen
    def all_zeros(self):
        rows = self._connection.execute('SELECT * FROM breeds WHERE count = 0')
        readable_breeds = []
        for row in rows:
            item = Breed(
                row["id"], row["breed_name"], row["count"],
            )
            readable_breeds.append(item)
        
        readable_breeds = "".join(
        f"""
        Breed name: {breed.breed_name}
        Count: {breed.count}
        """
        for breed in readable_breeds
    )
        return readable_breeds
    
    # Delete a breed entry
    def delete(self, id):
        self._connection.execute('DELETE FROM breeds WHERE id = %s', [id])
        return None
