from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.member import Member
from models.session import Session


class SessionListResource(Resource):
    def get(self):
        data = Session.get_all()
        if data is None:
            return {"message": "Session is not found"}, HTTPStatus.NOT_FOUND
        return {"data": data}, HTTPStatus.OK

    def post(self):
        data = request.get_json()

        member = Member.get_by_id(data["member_id"])
        if member is None:
            return {"message": "Member not found"}, HTTPStatus.NOT_FOUND

        if not member.is_trainer:
            return {"message": "Member is not trainer"}, HTTPStatus.NOT_FOUND

        session = Session(
            session_name=data["session_name"],
            session_date=data["session_date"],
            member_id=data["member_id"],
        )
        session.save()

        return session.data, HTTPStatus.CREATED


class SessionResources(Resource):
    def get(self, session_id):
        session = Session.get_by_id(session_id)
        if session is None:
            return {"message": "Session not found"}, HTTPStatus.NOT_FOUND
        return session.data, HTTPStatus.OK

    def put(self, session_id):
        data = request.get_json()
        return Session.update(session_id, data)


class SessionPublishResource(Resource):
    def put(self, session_id):
        return Session.publish(session_id)

    def delete(self, session_id):
        return Session.un_publish(session_id)
