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
        if phone is None:
            return {"message": "Phone number is required"}, HTTPStatus.BAD_REQUEST

        first_name = json_data.get("first_name")
        last_name = json_data.get("last_name")
        phone = json_data.get("phone_number")
        is_trainer = json_data.get(
            "is_trainer", False
        )  # Default will be False if not included

        # Do not add the user if the username is taken
        if Member.get_by_phone(phone):
            return {"message": "Phone number already used"}, HTTPStatus.BAD_REQUEST

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


class MemberResources(Resource):
    def get(self, member_id):
        member = Member.get_by_id(member_id)
        if member is None:
            return {"message": "member not found"}, HTTPStatus.NOT_FOUND
        return member.data, HTTPStatus.OK
