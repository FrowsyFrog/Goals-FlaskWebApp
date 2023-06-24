from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.lastname = data['lastname']
        self.email = data['email']
        self.password = data['password']

    def __init__(self, id, data):
        self.id = id
        self.name = data['name']
        self.lastname = data['lastname']
        self.email = data['email']
        self.password = data['password']