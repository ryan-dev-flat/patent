class UserResource(Resource):
    @cross_origin()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help="Username cannot be blank!")
        parser.add_argument('password', required=True, help="Password cannot be blank!")
        args = parser.parse_args()

        # Check if the username already exists
        if User.query.filter_by(username=args['username']).first():
            return {'error': 'Username already exists'}, 400

        new_user = User(username=args['username'], password=args['password'])
        db.session.add(new_user)
        try:
            db.session.commit()
            # Generate access token
            access_token = create_access_token(identity=args['username'])
            return jsonify({"message": "User registered successfully", "access_token": access_token}), 201
        except IntegrityError:
            db.session.rollback()
            return {'error': 'Username already exists'}, 400

    @jwt_required()
    @cross_origin()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user:
            return {'username': user.username}, 200
        return {'message': 'User not found'}, 404

    @jwt_required()
    @cross_origin()
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=False)
        parser.add_argument('password', required=False)
        args = parser.parse_args()

        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user:
            if args['username']:
                user.username = args['username']
            if args['password']:
                user.password = args['password']
            db.session.commit()
            return {'message': 'User updated successfully'}, 200
        return {'message': 'User not found'}, 404

    @jwt_required()
    @cross_origin()
    def delete(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}, 200
        return {'message': 'User not found'}, 404

    @cross_origin()
    def options(self):
        return '', 200