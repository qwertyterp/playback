from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager


# TODO: implement
@login_manager.user_loader
def load_user(user_id):
    #pass
    return User.objects(username=user_id).first()

# TODO: implement fields
class User(db.Document, UserMixin):
    email = db.EmailField(unique=True, required=True)
    username = db.StringField(unique=True, required=True)
    password = db.StringField()
    profile_pic = db.ImageField()

    # Returns unique string identifying our object
    def get_id(self):
        # TODO: implement
        return self.username

class Review(db.Document):
    commenter = db.ReferenceField(User)
    content = db.StringField(required= True,min_length=5, max_length=500 )
    date = db.StringField(required= True)
    album_id = db.StringField(required=True)
    album_title = db.StringField(required=True)
    #image = db.StringField()
    #Uncomment when other fields are ready for review pictures