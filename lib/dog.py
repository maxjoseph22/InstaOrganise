class Dog:
    def __init__(
        self,
        id,
        name,
        breed,
        purebreed,
        mix,
        age,
        sex,
        location,
        personality,
        likes,
        comments,
        link_to_post,
        photo=None  # Default to None for optional fields
    ):
        self.id = id
        self.name = name
        self.breed = breed
        self.purebreed = purebreed
        self.mix = mix
        self.age = age
        self.sex = sex
        self.location = location
        self.personality = personality
        self.likes = likes
        self.comments = comments
        self.link_to_post = link_to_post
        self.photo = photo

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return (
            f"<Dog(id={self.id}, name='{self.name}', breed='{self.breed}', "
            f"purebreed={self.purebreed}, mix={self.mix}, age={self.age}, "
            f"sex='{self.sex}', location='{self.location}', "
            f"personality='{self.personality}', likes={self.likes}, "
            f"comments={self.comments}, link_to_post='{self.link_to_post}', photo='{self.photo}')>"
        )
