class Breed:
    def __init__(self, id, breed_name, count):
        self.id = id
        self.breed_name = breed_name
        self.count = count

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return (
            f"<Breed(id={self.id}, breed_name='{self.breed_name}', count='{self.count}'>"
        )
