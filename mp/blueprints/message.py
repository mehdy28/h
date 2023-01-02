from flask import Blueprint, request, jsonify
from db import db
from models import MessageModel
from schemas.schemas import MessageSchema

messages_bp = Blueprint("messages", __name__)

@messages_bp.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()
    message = MessageModel(text=data['text'], user_id=data['user_id'], channel_id=data['channel_id'])
    db.session.add(message)
    db.session.commit()
    message_schema = MessageSchema()
    result = message_schema.dump(message)
    return jsonify({'message': result})

@messages_bp.route('/get-messages/<int:channel_id>', methods=['GET'])
def get_messages(channel_id):
    messages = MessageModel.query.filter_by(channel_id=channel_id).all()
    if messages:
        message_schema = MessageSchema(many=True)
        result = message_schema.dump(messages)
        return jsonify({'messages': result})
    else:
        return 'No messages found', 404

@messages_bp.route('/update-message/<int:message_id>', methods=['PUT'])
def update_message(message_id):
    message = MessageModel.query.get(message_id)
    if message:
        data = request.get_json()
        message.text = data['text']
        db.session.commit()
        message_schema = MessageSchema()
        result = message_schema.dump(message)
        return jsonify({'message': result})
    else:
        return 'Message not found', 404


@messages_bp.route('/delete-message/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    message = MessageModel.query.get(message_id)
    if message:
        db.session.delete(message)
        db.session.commit()
        return '', 204
    else:
        return 'Message not found', 404
