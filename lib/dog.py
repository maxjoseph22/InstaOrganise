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
        video,
        date_posted,
        photo=None,
        breed_id=None,
        cross_breed_id=None,
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
        self.video = video
        self.date_posted = date_posted
        self.photo = photo
        self.breed_id = breed_id
        self.cross_breed_id = cross_breed_id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return (
            f"<Dog(id={self.id}, name='{self.name}', breed='{self.breed}', "
            f"purebreed={self.purebreed}, mix={self.mix}, age={self.age}, "
            f"sex='{self.sex}', location='{self.location}', "
            f"personality='{self.personality}', likes={self.likes}, "
            f"comments={self.comments}, link_to_post='{self.link_to_post}', " f"video='{self.video}', "
            f"photo='{self.photo}', date_posted={self.date_posted}, breed_id={self.breed_id}), cross_breed_id={self.cross_breed_id}>"
        )
