from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()
    email = fields.Str()
    password = fields.Str()



class ChannelSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    is_private = fields.Bool()



class MessageSchema(Schema):
    id = fields.Int()
    text = fields.Str()
    timestamp = fields.DateTime()
    user_id = fields.Int()
    channel_id = fields.Int()



class MembershipSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    channel_id = fields.Int()
