#models.py
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship, validates
from sqlalchemy_serializer import SerializerMixin
from utils import fetch_patent_grants

db = SQLAlchemy()
    
user_patent = db.Table(
    'user_patent',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('patent_id', db.Integer, db.ForeignKey('patent.id'), primary_key=True)
)


class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    patents = db.relationship('Patent', secondary=user_patent, back_populates='users')

    
    def __repr__(self):
        return f'<User {self.username}>'


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


class Patent(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    patentability_score = db.Column(db.Float)
    status = db.Column(db.String(64), nullable=False, default='Pending')
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    users = db.relationship('User', secondary=user_patent, back_populates='patents')  # Use back_populates
    utility = db.relationship('Utility', uselist=False, back_populates='patent')
    novelty = db.relationship('Novelty', uselist=False, back_populates='patent')
    obviousness = db.relationship('Obviousness', uselist=False, back_populates='patent')
    prior_art = db.relationship('PriorArt', back_populates='patent')

    def __repr__(self):
        return f'<Patent {self.title}, {self.description}>'

    def calculate_patentability_score(self):
        novelty_score = self.novelty.calculate_novelty_score() if self.novelty else 0
        utility_score = self.utility.calculate_utility_score() if self.utility else 0
        obviousness_score = self.obviousness.calculate_obviousness_score() if self.obviousness else 0
        patentability_score = (novelty_score * 0.4) + (utility_score * 0.3) + (obviousness_score * 0.3)
        self.patentability_score = patentability_score
        return patentability_score

   

class PriorArt(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    patent_number = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    abstract = db.Column(db.Text, nullable=False)
    url = db.Column(db.String, nullable=False)
    patent_id = db.Column(db.Integer, db.ForeignKey('patent.id'))
    patent = db.relationship('Patent', back_populates='prior_art')

    def fetch_and_store_prior_art(self, description):
        prior_art_data = fetch_patent_grants(description)
        if prior_art_data:
            for data in prior_art_data:
                prior_art = PriorArt(
                    patent_number=data['patent_number'],
                    title=data['title'],
                    abstract=data['abstract'],
                    url=data['url'],
                    patent_id=self.patent_id
                )
                db.session.add(prior_art)
            db.session.commit()




class Utility(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    useful = db.Column(db.Boolean)
    operable = db.Column(db.Boolean)
    practical = db.Column(db.Boolean)
    utility_score = db.Column(db.Float)
    patent_id = db.Column(db.Integer, db.ForeignKey('patent.id'))
    patent = db.relationship('Patent', back_populates='utility')

    def calculate_utility_score(self):
        score = 0.05
        if self.useful:
            score += 0.4
        if self.operable:
            score += 0.3
        if self.practical:
            score += 0.3
        self.utility_score = score
        return self.utility_score

class Novelty(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    new_invention = db.Column(db.Boolean)
    not_publicly_disclosed = db.Column(db.Boolean)
    not_described_in_printed_publication = db.Column(db.Boolean)
    not_in_public_use = db.Column(db.Boolean)
    not_on_sale = db.Column(db.Boolean)
    novelty_score = db.Column(db.Float)
    patent_id = db.Column(db.Integer, db.ForeignKey('patent.id'))
    patent = db.relationship('Patent', back_populates='novelty')

    def calculate_novelty_score(self):
        score = 1.0
        if not self.new_invention:
            score -= 0.3
        if not self.not_publicly_disclosed:
            score -= 0.2
        if not self.not_described_in_printed_publication:
            score -= 0.2
        if not self.not_in_public_use:
            score -= 0.15
        if not self.not_on_sale:
            score -= 0.15
        self.novelty_score = max(0, score)
        return self.novelty_score

class Obviousness(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    scope_of_prior_art = db.Column(db.String)
    differences_from_prior_art = db.Column(db.String)
    level_of_ordinary_skill = db.Column(db.String)
    secondary_considerations = db.Column(db.String)
    obviousness_score = db.Column(db.Float)
    patent_id = db.Column(db.Integer, db.ForeignKey('patent.id'))
    patent = db.relationship('Patent', back_populates='obviousness')

    def calculate_obviousness_score(self):
        score = 1.0
        
        # Scope of prior art
        if self.scope_of_prior_art == "Very similar":
            score -= 0.3
        elif self.scope_of_prior_art == "Somewhat similar":
            score -= 0.2
        elif self.scope_of_prior_art == "Different field":
            score -= 0.1

        # Differences from prior art
        if self.differences_from_prior_art == "Minor":
            score -= 0.3
        elif self.differences_from_prior_art == "Moderate":
            score -= 0.2
        elif self.differences_from_prior_art == "Significant":
            score -= 0.1

        # Level of ordinary skill
        if self.level_of_ordinary_skill == "High":
            score -= 0.2
        elif self.level_of_ordinary_skill == "Medium":
            score -= 0.1

        # Secondary considerations
        if self.secondary_considerations:
            score += 0.1

        self.obviousness_score = max(0, score)
        return self.obviousness_score