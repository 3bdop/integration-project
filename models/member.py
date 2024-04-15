from extensions import db
from http import HTTPStatus


# User Attributes
class Member(db.Model):
    __tablename__ = "member"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False, unique=False)
    last_name = db.Column(db.String(45), nullable=True, unique=False)
    phone_number = db.Column(db.String(20), nullable=False, unique=True)
    is_trainer = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(),
        nullable=False,
        server_default=db.func.now(),
        onupdate=db.func.now(),
    )

    # recipes = db.relationship("Recipe", backref="user")

    @property
    def data(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,  # Convert date to ISO format for JSON serialization
            "is_trainer": self.is_trainer,
        }

    # A static method to get a user data by the id
    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    # A static method to get a user data by the phone number
    @classmethod
    def get_by_phone(cls, phone):
        return cls.query.filter_by(phone_number=phone).first()

    @classmethod
    def get_all(cls):
        r = cls.query.all()

        result = []

        for i in r:
            result.append(i.data)

        return result

    @classmethod
    def update(cls, id, data):
        member_obj = cls.query.filter(cls.id == id).first()
        if not member_obj:
            return {"message": "Member not found"}, HTTPStatus.NOT_FOUND

        member_obj.first_name = data["first_name"]
        member_obj.last_name = data["last_name"]
        phone = data["phone_number"]
        if phone:
            member_obj.phone_number = phone

        if Member.get_by_phone(phone):
            return {"message": "Phone number already used!"}, HTTPStatus.BAD_REQUEST

        member_obj.is_trainer = data["is_trainer"]

        db.session.commit()
        return member_obj.data, HTTPStatus.OK

    @classmethod
    def delete(cls, id):
        member_obj = cls.query.filter(cls.id == id).first()
        if not member_obj:
            return {"message": "Member not found"}, HTTPStatus.NOT_FOUND

        db.session.delete(member_obj)
        db.session.commit()
        return {}, HTTPStatus.NO_CONTENT

    # Save the record
    def save(self):
        db.session.add(self)
        db.session.commit()
