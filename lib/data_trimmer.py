# Example data (string)

# Dipper, Pit Bull (13 y/o), Red Bank, NJ. 
# "He loves to chew our socks and sleep on the couch,
# when he was a puppy he was very energetic but now
# he's kinda goofy and sleeps all day".

class Data:
    def __init__(self, id, data_string):
        self.id = id
        self.data_string = data_string

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    
    def __repr__(self):
        return f"Data({self.id}, {self.data_string})"


