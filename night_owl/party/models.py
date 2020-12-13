from night_owl import db

party_image = db.Table(
    "party_image",
    db.Model.metadata,
    db.Column("party_id", db.Integer, db.ForeignKey("party.id")),
    db.Column("image_id", db.Integer, db.ForeignKey("image.id")),
)


class Party(db.Model):
    __tablename__ = "party"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(256), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(280), nullable=False)
    images = db.relationship(
        "Image",
        secondary=party_image,
        back_populates="parties",
    )
    name = db.Column(db.String(64), nullable=False)
    reviews = db.relationship("Review", cascade="delete")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "admin_id": self.admin_id,
            "images": [i.serialize() for i in self.images],
        }