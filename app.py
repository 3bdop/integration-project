import sys
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from config import Config
from extensions import db

from resources.member_session import (
    MemberSessionListResource,
    MemberSessionResources,
)
from resources.member import MemberListResource, Member, MemberResources
from resources.session import (
    SessionListResource,
    SessionResources,
    SessionPublishResource,
)


def create_app():
    print("Hello", file=sys.stderr)
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_resources(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)


def register_resources(app):
    api = Api(app)

    api.add_resource(MemberListResource, "/members")
    api.add_resource(MemberResources, "/members/<int:member_id>")
    api.add_resource(SessionListResource, "/sessions")
    api.add_resource(SessionResources, "/sessions/<int:session_id>")
    api.add_resource(SessionPublishResource, "/sessions/<int:session_id>/publish")
    api.add_resource(MemberSessionListResource, "/member-session")
    api.add_resource(MemberSessionResources, "/member-session/<int:msession_id>")


if __name__ == "__main__":
    app = create_app()
    app.run("127.0.0.1", 5000)
