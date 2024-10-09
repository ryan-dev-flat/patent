from .models import *


db = SQLAlchemy()

class Patent(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    patentability_score = db.Column(db.Float)
    status = db.Column(db.String(64), nullable=False, default='Pending')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', secondary='user_patent', back_populates='patents')
    utility = db.relationship('Utility', uselist=False, back_populates='patent')
    novelty = db.relationship('Novelty', uselist=False, back_populates='patent')
    obviousness = db.relationship('Obviousness', uselist=False, back_populates='patent')
    prior_art = db.relationship('PriorArt', uselist=False, back_populates='patent')

    def __repr__(self):
        return f'<Patent {self.title}, {self.description}>'

    def calculate_patentability_score(self):
        novelty_score = self.novelty.calculate_novelty_score()
        utility_score = self.utility.calculate_utility_score()
        obviousness_score = self.obviousness.calculate_obviousness_score()
        patentability_score = (novelty_score * 0.4) + (utility_score * 0.3) + (obviousness_score * 0.3)
        self.patentability_score = patentability_score
        return patentability_score

user_patent = db.Table('user_patent',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('patent_id', db.Integer, db.ForeignKey('patent.id'), primary_key=True)
)