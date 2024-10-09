from models import db, SerializerMixin
from sqlalchemy.orm import validates
from patent_model import Patent


class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    patents = db.relationship('Patent', secondary='user_patent', back_populates='user')

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username cannot be empty")
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long")
        return username

    @validates('password')
    def validate_password(self, key, password):
        if not password:
            raise ValueError("Password cannot be empty")
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return password

    def __repr__(self):
        return f'<User {self.username}>'