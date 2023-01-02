from flask import Blueprint, request, jsonify
from db import db
from models import MembershipModel
from schemas.schemas import MembershipSchema

memberships_bp = Blueprint("memberships", __name__)
@memberships_bp.route('/join-channel', methods=['POST'])
def join_channel():
    data = request.get_json()
    membership = MembershipModel(user_id=data['user_id'], channel_id=data['channel_id'])
    db.session.add(membership)
    db.session.commit()
    membership_schema = MembershipSchema()
    result = membership_schema.dump(membership)
    return jsonify({'membership': result})

@memberships_bp.route('/get-channel-members/<int:channel_id>', methods=['GET'])
def get_channel_members(channel_id):
    memberships = MembershipModel.query.filter_by(channel_id=channel_id).all()
    if memberships:
        membership_schema = MembershipSchema(many=True)
        result = membership_schema.dump(memberships)
        return jsonify({'memberships': result})
    else:
        return 'No members found', 404
    
@memberships_bp.route('/update-membership/<int:membership_id>', methods=['PUT'])
def update_membership(membership_id):
    membership = MembershipModel.query.get(membership_id)
    if membership:
        data = request.get_json()
        membership.user_id = data['user_id']
        membership.channel_id = data['channel_id']
        db.session.commit()
        membership_schema = MembershipSchema()
        result = membership_schema.dump(membership)
        return jsonify({'membership': result})
    else:
        return 'Membership not found', 404

@memberships_bp.route('/delete-membership/<int:membership_id>', methods=['DELETE'])
def delete_membership(membership_id):
    membership = MembershipModel.query.get(membership_id)
    if membership:
        db.session.delete(membership)
        db.session.commit()
        return '', 204
    else:
        return 'Membership not found', 404

