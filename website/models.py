from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, data):
        self.id = data[0]
        self.name = data[1]
        self.lastname = data[2]
        self.email = data[3]
        self.password = data[4]