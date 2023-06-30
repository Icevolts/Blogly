"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE = 'https://upload.wikimedia.org/wikipedia/commons/2/2c/Default_pfp.svg'

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    '''User info'''
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    
    first_name = db.Column(db.Text,
                           nullable = False)
    
    last_name = db.Column(db.Text,
                          nullable = False)
    
    image_url = db.Column(db.Text,
                          nullable = False,
                          default = DEFAULT_IMAGE)
    
    @property
    def full_name(self):
        '''Return users full name for querying'''
        return f"{self.first_name} {self.last_name}"