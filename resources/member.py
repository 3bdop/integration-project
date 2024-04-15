from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.member import Member


class MemberListResource(Resource):
    def get(self):
        data = Member.get_all()
        if data is None:
            return {"message": "Member is not found"}, HTTPStatus.NOT_FOUND
        return {"data": data}, HTTPStatus.OK

    def post(self):
        json_data = request.get_json()

        phone = json_data.get("phone_number")
        if phone is None or phone == "":
            return {"message": "Phone number is required"}, HTTPStatus.BAD_REQUEST

        first_name = json_data.get("first_name")
        last_name = json_data.get("last_name")
        phone = json_data.get("phone_number")
        is_trainer = json_data.get(
            "is_trainer", False
        )  # Default will be False if not included

        # Do not add the user if the phone is taken
        if Member.get_by_phone(phone):
            return {"message": "Phone number already used"}, HTTPStatus.BAD_REQUEST

        if is_trainer is None or is_trainer not in [True, False]:
            return {
                "message": "is_trainer field must exist and be True or False"
            }, HTTPStatus.BAD_REQUEST

        member = Member(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone,
            is_trainer=is_trainer,
        )

        member.save()

        data = {
            "id": member.id,
            "first_name": member.first_name,
            "last_name": member.last_name,
            "phone_number": member.phone_number,
            "is_trainer": member.is_trainer,
        }

        return data, HTTPStatus.CREATED


from models.session import Session

# from models.member_session import MemberHasSession


class MemberResources(Resource):
    def get(self, member_id):
        member = Member.get_by_id(member_id)
        if member is None:
            return {"message": "member not found"}, HTTPStatus.NOT_FOUND
        return member.data, HTTPStatus.OK

    def put(self, member_id):
        member = Member.get_by_id(member_id)
        if member is None:
            return {"message": "member not found"}, HTTPStatus.NOT_FOUND

        data = request.get_json()
        return (Member.update(member_id, data),)

    def delete(self, member_id):
        member = Member.get_by_id(member_id)
        if member is None:
            return {"message": "member not found"}, HTTPStatus.NOT_FOUND

        # Check if the member is associated with any session as a trainer
        sessions_with_trainer = Session.query.filter_by(member_id=member_id).all()
        if sessions_with_trainer:
            return {
                "message": "Member is associated with sessions as a trainer. Remove the member from the sessions or delete the sessions first."
            }, HTTPStatus.BAD_REQUEST

        # member_has_session = MemberHasSession.get_by_member_id(member_id)
        # if member_has_session:
        #     return {
        #         "message": "Member is associated with sessions. Remove the member from the sessions or delete the sessions first."
        #     }, HTTPStatus.BAD_REQUEST

        return Member.delete(member_id)
