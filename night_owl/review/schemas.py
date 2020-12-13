from marshmallow import Schema, fields, validate


class ReviewSchema(Schema):
    rating = fields.Float(required=True)
    comment = fields.Str(
        validate=validate.Length(min=1, max=280),
        allow_none=True,
        required=False,
    )
    images = fields.List(
        fields.Raw(allow_none=True),
        required=False,
    )
