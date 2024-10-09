from models import *

class Utility(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    operability = db.Column(db.Boolean)
    beneficial = db.Column(db.Boolean)
    practical = db.Column(db.Boolean)
    utility_score = db.Column(db.Float)
    patent_id = db.Column(db.Integer, db.ForeignKey('patent.id'))
    patent = db.relationship('Patent', back_populates='utility')

    def calculate_utility_score(self):
        score = 0.0
        if self.operability:
            score += 0.4
        if self.beneficial:
            score += 0.3
        if self.practical:
            score += 0.3
        self.utility_score = score
        return self.utility_score