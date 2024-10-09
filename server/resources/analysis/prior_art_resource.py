from models import *

class PriorArtResource(Resource):
    @jwt_required()
    def post(self, patent_id):
        current_user = get_jwt_identity()
        
        # Retrieve the patent belonging to the current user
        patent = Patent.query.filter_by(id=patent_id, user_id=current_user).first()
        
        if not patent:
            return {'message': 'Patent not found or does not belong to the user'}, 404
        
        # Extract keywords from the patent description
        description = patent.description  
        keywords = extract_keywords(description)
        
        # Fetch and store prior art using the method in the PriorArt model
        prior_art_instance = PriorArt(patent_id=patent_id)
        prior_art_instance.fetch_and_store_prior_art(keywords)
        
        # Retrieve the stored prior art
        prior_art = PriorArt.query.filter_by(patent_id=patent_id).all()
        
        if not prior_art:
            return {'message': 'No prior art found for this patent'}, 404
        
        prior_art_list = [{'patent_number': art.patent_number, 'title': art.title, 'abstract': art.abstract, 'url': art.url} for art in prior_art]
        
        return jsonify({'prior_art': prior_art_list})
    
    @cross_origin()
    def options(self):
        return '', 200