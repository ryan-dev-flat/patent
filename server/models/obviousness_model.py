from models import *


class Obviousness(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    prior_art_scope = db.Column(db.String, nullable=False)
    differences = db.Column(db.String, nullable=False)
    skill_level = db.Column(db.String, nullable=False)
    secondary_considerations = db.Column(db.String)
    obviousness_score = db.Column(db.Float)
    
    patent_id = db.Column(db.Integer, db.ForeignKey('patent.id'))
    patent = db.relationship('Patent', back_populates='obviousness')

    def calculate_obviousness_score(self):
        score = 1.0
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