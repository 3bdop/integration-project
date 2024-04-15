import sys
from extensions import db
from resources.member import MemberListResource
from resources.session import SessionListResource
from resources.session import SessionResources
from models.member import Member
from models.session import Session
from http import HTTPStatus


class MemberHasSession(db.Model):
    __tablename__ = "member_session"

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("member.id"), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey("session.id"), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(),
        nullable=False,
        server_default=db.func.now(),
        onupdate=db.func.now(),
    )

    @property
    def data(self):
        return {
            "id": self.id,
            "member_id": self.member_id,
            "session_id": self.session_id,
        }

    @classmethod
    def get_all(cls):
        member_has_session = cls.query.all()
        return [mhc.data for mhc in member_has_session]

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_by_member_id(cls, member_id):
        return cls.query.filter_by(member_id=member_id).all()

    @classmethod
    def delete(cls, id):
        mhc = cls.query.get(id)
        if not mhc:
            return {"message": "MemberHasClass not found"}, HTTPStatus.NOT_FOUND

        db.session.delete(mhc)
        db.session.commit()
        return {}, HTTPStatus.NO_CONTENT

    def save(self):
        db.session.add(self)
        db.session.commit()

    # @classmethod
    # def update(cls, id, data):
    #     msession = cls.query.filter(cls.id == id).first()
    #     if msession is None:
    #         return {"message": "Member session not found"}, HTTPStatus.NOT_FOUND

    #     msession.member_id = data["member_id"]
    #     msession.session_id = data["session_id"]

    #     db.session.commit()
    #     return msession.data, HTTPStatus.OK
