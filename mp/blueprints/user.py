import uuid
from flask import Blueprint, request, jsonify
from db import db
from models import UserModel
from schemas.schemas import UserSchema

users_bp = Blueprint("users", __name__)

@users_bp.route('/create-user', methods=['POST'])
def create_user():
    data = request.get_json()
    user = UserModel(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    user_schema = UserSchema()
    result = user_schema.dump(user)
    return jsonify({'user': result})


@users_bp.route('/get-user-info/<int:user_id>', methods=['GET'])
def get_user_info(user_id):
    user = UserModel.query.get(user_id)
    if user:
        user_schema = UserSchema()
        result = user_schema.dump(user)
        return jsonify({'user': result})
    else:
        return 'User not found', 404
    
@users_bp.route('/user', methods=['GET'])
def get_all_users():
    users = UserModel.query.all()
    user_schema = UserSchema(many=True)
    result = user_schema.dump(users)
    return jsonify({'users': result})