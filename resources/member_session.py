import sys
from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.member import Member
from models.member_session import MemberHasSession
from models.session import Session


class MemberSessionListResource(Resource):
    def get(self):
        data = MemberHasSession.get_all()
        if data is None:
            return {"message": "Member Session not found"}, HTTPStatus.NOT_FOUND
        return {"data": data}

    def post(self):
        data = request.get_json()
        member_id = data["member_id"]
        member_id = Member.get_by_id(member_id)
        print(member_id)
        session_id = data["session_id"]
        session_id = Session.get_by_id(session_id)
        print(session_id)

        if member_id is None or session_id is None:
            return {"message": "member or session does not exist"}, HTTPStatus.NOT_FOUND

        if member_id.is_trainer:
            return {"message": "can not register a trainer"}, HTTPStatus.BAD_REQUEST

        msession = MemberHasSession(
            member_id=data["member_id"], session_id=data["session_id"]
        )

        msession.save()
        return msession.data, HTTPStatus.CREATED


class MemberSessionResources(Resource):
    def get(self, msession_id):
        msession = MemberHasSession.get_by_id(msession_id)
        if msession is None:
            return {"message": "member session not found"}, HTTPStatus.NOT_FOUND
        return msession.data, HTTPStatus.OK

    # def put(self, msession_id):
    #     data = request.get_json()
    #     return MemberHasSession.u

    def delete(self, msession_id):
        msession = MemberHasSession.get_by_id(msession_id)
        if msession is None:
            return {"message": "member session not found"}, HTTPStatus.NOT_FOUND

        return MemberHasSession.delete(msession_id)
