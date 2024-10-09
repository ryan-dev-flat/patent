from models import *


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
    
    patent_id = db.Column(db.Integer, db.ForeignKey('patent.id'))
    patent = db.relationship('Patent', back_populates='novelty')

    def calculate_novelty_score(self):
        score = 1.0
        if self.patented or self.printed_pub or self.public_use or self.on_sale or self.publicly_available or self.patent_app:
            score -= 0.2
        if self.inventor_underoneyear:
            score += 0.1
        self.novelty_score = max(0, score)
        return self.novelty_score