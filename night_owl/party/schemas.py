from marshmallow import fields, Schema, validate


class PartySchema(Schema):
    name = fields.Str(
        validate=validate.Length(min=1, max=64),
        required=True,
    )
    datetime = fields.DateTime(required=True)
    address = fields.Str(
        validate=validate.Length(min=1, max=256),
        required=True,
    )
    description = fields.Str(
        validate=validate.Length(min=1, max=280),
        required=True,
    )
    admin_id = fields.Int(required=True)
    images = fields.List(fields.Raw(allow_none=True))
