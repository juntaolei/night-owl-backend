from night_owl import db
from night_owl.party import party_image
from night_owl.review import review_image


class Image(db.Model):
    __tablename__ = "image"

    id = db.Column(db.Integer, primary_key=True)
    parties = db.relationship(
        "Party",
        secondary=party_image,
        back_populates="images",
    )
    reviews = db.relationship(
        "Review",
        secondary=review_image,
        back_populates="images",
    )
    url = db.Column(db.String, nullable=False)

    def serialize(self):
        return {"url": self.url}