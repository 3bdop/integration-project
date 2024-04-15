import sys
from extensions import db
from resources.member import MemberListResource
from models.member import Member
from http import HTTPStatus


class Session(db.Model):
    __tablename__ = "session"

    id = db.Column(db.Integer, primary_key=True)
    session_name = db.Column(db.String(100), nullable=False)
    session_date = db.Column(db.Date, nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey("member.id"), nullable=False)
    is_publish = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(),
        nullable=False,
        server_default=db.func.now(),
        onupdate=db.func.now(),
    )

    @property
    def data(self):
        member = Member.get_by_id(self.member_id)
        member_data = {
            "id": member.id,
            "first_name": member.first_name,
            "last_name": member.last_name,
            "phone_number": member.phone_number,
        }
        return {
            "id": self.id,
            "session_name": self.session_name,
            "session_date": self.session_date.isoformat(),  # Convert date to ISO format for JSON serialization
            "trainer": member_data,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        r = cls.query.filter_by(is_publish=True).all()

        result = []

        for i in r:
            result.append(i.data)

        return result

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter((cls.id == id) & (cls.is_publish == True)).first()

    @classmethod
    def get_by_id_n(cls, id):
        x = cls.query.filter((cls.id == id) & (cls.is_publish == False)).first()
        return x

    @classmethod
    def update(cls, id, data):
        session_obj = cls.query.filter(cls.id == id).first()
        if not session_obj:
            return {"message": "Session not found"}, HTTPStatus.NOT_FOUND

        session_obj.session_name = data["session_name"]
        session_obj.session_date = data["session_date"]
        session_obj.member_id = data["member_id"]
        db.session.commit()
        return session_obj.data, HTTPStatus.OK

    @classmethod
    def delete(cls, id):
        session_obj = cls.query.filter(cls.id == id).first()
        if not session_obj:
            return {"message": "session not found"}, HTTPStatus.NOT_FOUND

        db.session.delete(session_obj)
        db.session.commit()
        return {}, HTTPStatus.NO_CONTENT

    @classmethod
    def publish(cls, session_id):
        session = Session.get_by_id_n(session_id)
        if session is None:
            return {"message": "session not found"}, HTTPStatus.NOT_FOUND

        session.is_publish = True
        db.session.commit()
        return session.data, HTTPStatus.OK

    @classmethod
    def un_publish(cls, session_id):
        session = Session.get_by_id(session_id)
        if session is None:
            return {"message": "session not found"}, HTTPStatus.NOT_FOUND

        session.is_publish = False
        db.session.commit()
        return session.data, HTTPStatus.OK
