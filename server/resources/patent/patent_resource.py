class PatentResource(Resource):
    @jwt_required()
    @cross_origin()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True, help="Title cannot be blank!")
        parser.add_argument('description', required=True, help="Description cannot be blank!")
        args = parser.parse_args()

        user_id = get_jwt_identity()
        new_patent = Patent(title=args['title'], description=args['description'], user_id=user_id)
        db.session.add(new_patent)
        db.session.commit()

        return {'message': 'Patent created successfully'}, 201

    @jwt_required()
    @cross_origin()
    def get(self, patent_id=None):
        user_id = get_jwt_identity()
        if patent_id:
            patent = Patent.query.filter_by(id=patent_id, user_id=user_id).first()
            if patent:
                return {'id': patent.id, 'title': patent.title, 'description': patent.description}, 200
            return {'message': 'Patent not found'}, 404
        else:
            patents = Patent.query.filter_by(user_id=user_id).all()
            return [{'id': patent.id, 'title': patent.title, 'description': patent.description} for patent in patents], 200

    @jwt_required()
    @cross_origin()
    def patch(self, patent_id):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=False)
        parser.add_argument('description', required=False)
        args = parser.parse_args()

        user_id = get_jwt_identity()
        patent = Patent.query.filter_by(id=patent_id, user_id=user_id).first()
        if patent:
            if args['title']:
                patent.title = args['title']
            if args['description']:
                patent.description = args['description']
            db.session.commit()
            return {'message': 'Patent updated successfully'}, 200
        return {'message': 'Patent not found'}, 404

    @jwt_required()
    @cross_origin()
    def delete(self, patent_id):
        user_id = get_jwt_identity()
        patent = Patent.query.filter_by(id=patent_id, user_id=user_id).first()
        if patent:
            db.session.delete(patent)
            db.session.commit()
            return {'message': 'Patent deleted successfully'}, 200
        return {'message': 'Patent not found'}, 404
