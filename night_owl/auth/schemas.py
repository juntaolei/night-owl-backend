from marshmallow import fields, Schema, validate


class RegistrationSchema(Schema):
    email = fields.Email(
        validate=validate.Length(min=1, max=64),
        required=True,
    )
    first_name = fields.Str(
        validate=validate.Length(min=1, max=64),
        required=True,
    )
    last_name = fields.Str(
        validate=validate.Length(min=1, max=64),
        required=True,
    )
    username = fields.Str(
        validate=validate.Length(min=1, max=64),
        required=True,
    )
    password = fields.Str(
        validate=validate.Length(min=12, max=64),
        required=True,
    )


class LoginSchema(Schema):
    username = fields.Str(
        validate=validate.Length(min=1, max=64),
        required=True,
    )
    password = fields.Str(
        validate=validate.Length(min=12, max=64),
        required=True,
    )
