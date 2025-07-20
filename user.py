from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, google_id, email, name, picture, urls_remaining=10):
        self.id = id
        self.google_id = google_id
        self.email = email
        self.name = name
        self.picture = picture
        self.urls_remaining = urls_remaining

    def get_id(self):
        return str(self.id)
    
    def can_create_url(self):
        return self.urls_remaining > 0
    
    def is_premium(self):
        return self.urls_remaining > 10  # Premium users have more than the basic 10 links
