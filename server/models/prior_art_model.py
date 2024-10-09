from models import *

from prior_art_resource import PriorArtResource


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