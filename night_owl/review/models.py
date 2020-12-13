from night_owl import db

review_image = db.Table(
    "review_image",
    db.Model.metadata,
    db.Column("review_id", db.Integer, db.ForeignKey("review.id")),
    db.Column("image_id", db.Integer, db.ForeignKey("image.id")),
)


class Review(db.Model):
    __tablename__ = "review"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(280), nullable=True)
    images = db.relationship(
        "Image",
        secondary=review_image,
        back_populates="reviews",
    )
    party_id = db.Column(db.Integer, db.ForeignKey("party.id"), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def serialize(self):
        return {
            "party_id": self.party_id,
            "rating": self.rating,
            "comment": self.comment,
            "images": [i.serialize() for i in self.images],
        }