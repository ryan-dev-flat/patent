from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

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

class Patent(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    patentability_score = db.Column(db.Float)

    user = db.relationship('User', secondary='user_patent', back_populates='patents')
    utility = db.relationship('Utility', uselist=False, back_populates='patent')
    novelty = db.relationship('NoveltyTest', uselist=False, back_populates='patent')
    obviousness = db.relationship('Obviousness', uselist=False, back_populates='patent')
    prior_art = db.relationship('PriorArtSearch', uselist=False, back_populates='patent')

    def __repr__(self):
        return f'<Patent {self.title}>'

    def calculate_patentability_score(patent):
        novelty_score = patent.novelty.calculate_novelty_score()
        utility_score = patent.utility.calculate_utility_score()
        obviousness_score = patent.obviousness.calculate_obviousness_score()
        patentability_score = (novelty_score * 0.4) + (utility_score * 0.3) + (obviousness_score * 0.3)
        patent.patentability_score = patentability_score
        return patentability_score


user_patent = db.Table('user_patent',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('patent_id', db.Integer, db.ForeignKey('patent.id'), primary_key=True)
)

class Utility(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    operability = db.Column(db.Boolean)
    beneficial = db.Column(db.Boolean)
    practical = db.Column(db.Boolean)
    utility_score = db.Column(db.Boolean)

    def calculate_utility_score(self):
        # scoring logic
        score = 0.0
        if self.operability:
            score += 0.4
        if self.beneficial:
            score += 0.3
        if self.practical:
            score += 0.3
        self.utility_score = score
        return self.utility_score

class PriorArt(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    elements = db.Column(db.String)
    key_words = db.Column(db.String)
    patent_search = db.Column(db.String)
    publications = db.Column(db.String)
    public_disclosures = db.Column(db.String)

class Novelty(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    patented = db.Column(db.Boolean)
    printed_pub = db.Column(db.Boolean)
    public_use = db.Column(db.Boolean)
    on_sale = db.Column(db.Boolean)
    publicly_available = db.Column(db.Boolean)
    patent_app = db.Column(db.Boolean)
    inventor_underoneyear = db.Column(db.Boolean)
    novelty_score = db.Column(db.Float)

    def calculate_novelty_score(self):
        #  Scoring logic
        score = 1.0
        if self.patented or self.printed_pub or self.public_use or self.on_sale or self.publicly_available or self.patent_app:
            score -= 0.2
        if self.inventor_underoneyear:
            score += 0.1
        self.novelty_score = max(0, score)
        return self.novelty_score


class Obviousness(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    prior_art_scope = db.Column(db.String, nullable=False)
    differences = db.Column(db.String, nullable=False)
    skill_level = db.Column(db.String, nullable=False)
    secondary_considerations = db.Column(db.String)
    obviousness_score = db.Column(db.Float)

def calculate_obviousness_score(self):
        # Example scoring logic
        score = 1.0
        # Adjust score based on prior art scope, differences, skill level, and secondary considerations
      # add more complex logic
        if "significant" in self.prior_art_scope:
            score -= 0.3
        if "minor" in self.differences:
            score -= 0.2
        if "high" in self.skill_level:
            score -= 0.2
        if self.secondary_considerations:
            score += 0.1
        self.obviousness_score = max(0, score)
        return self.obviousness_score


