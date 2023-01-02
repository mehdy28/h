from blueprints.user import *

@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = UserModel.query.filter_by(email=data['email']).first()
    if user and user.password == data['password']:
        # Generate an API token for the user
        api_token = str(uuid.uuid4())
        user.api_token = api_token
        db.session.commit()
        user_schema = UserSchema()
        result = user_schema.dump(user)
        return jsonify({'user': result, 'api_token': api_token})
    else:
        return 'Invalid email or password', 401
