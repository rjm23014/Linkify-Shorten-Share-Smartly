from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, google_id, email, name, picture):
        self.id = id
        self.google_id = google_id
        self.email = email
        self.name = name
        self.picture = picture

    def get_id(self):
        return str(self.id)
