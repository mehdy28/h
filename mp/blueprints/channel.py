import uuid
from flask import Blueprint, request, jsonify
from db import db
from models import ChannelModel
from schemas.schemas import ChannelSchema

channels_bp = Blueprint("channels", __name__)

@channels_bp.route('/create-channel', methods=['POST'])
def create_channel():
    data = request.get_json()
    channel = ChannelModel(name=data['name'], description=data['description'], is_private=data['is_private'])
    db.session.add(channel)
    db.session.commit()
    channel_schema = ChannelSchema()
    result = channel_schema.dump(channel)
    return jsonify({'channel': result})

@channels_bp.route('/get-channel-info/<int:channel_id>', methods=['GET'])
def get_channel_info(channel_id):
    channel = ChannelModel.query.get(channel_id)
    if channel:
        channel_schema = ChannelSchema()
        result = channel_schema.dump(channel)
        return jsonify({'channel': result})
    else:
        return 'Channel not found', 404

@channels_bp.route('/update-channel/<int:channel_id>', methods=['PUT'])
def update_channel(channel_id):
    channel = ChannelModel.query.get(channel_id)
    if channel:
        data = request.get_json()
        channel.name = data['name']
        channel.description = data['description']
        channel.is_private = data['is_private']
        db.session.commit()
        channel_schema = ChannelSchema()
        result = channel_schema.dump(channel)
        return jsonify({'channel': result})
    else:
        return 'Channel not found', 404

@channels_bp.route('/delete-channel/<int:channel_id>', methods=['DELETE'])
def delete_channel(channel_id):
    channel = ChannelModel.query.get(channel_id)
    if channel:
        db.session.delete(channel)
        db.session.commit()
        return '', 204
    else:
        return 'Channel not found', 404
