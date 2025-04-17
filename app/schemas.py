from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    role = fields.Str()

class WarehouseSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    area = fields.Float()
    price = fields.Float()
    manager_id = fields.Int(allow_none=True)
