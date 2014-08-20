import json
from flask import request, g
from flask.ext.restful import Resource, reqparse
from AuthAPI.decorators import *
from AuthAPI.responses import *
from AuthAPI.services import commonsense


class Login(Resource):
    method_decorators = [decorators.application_verification,]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type = str, required = True, location='json')
        self.reqparse.add_argument('password', type = str, required = True, location='json')
        super(Login, self).__init__()

    def post(self):

        data = self.reqparse.parse_args()

        username = data["username"]

        if hasattr(g,'_application'):
            username = username + "@" + str(g._application.suffix)

        result, err = commonsense.login_user(username, data['password'])

        if not err:
            session_id = json.loads(result)
            return session_id, 200, {'X-SESSION-ID': session_id['session_id']}
        else:
            return respond(e_user_not_found)
