from flask import request, g, make_response
from flask.ext.restful import reqparse
from functools import wraps, update_wrapper
from AuthAPI.responses import *
from AuthAPI.models.applications import *
from AuthAPI.services import commonsense

auth_reqparse = reqparse.RequestParser()
auth_reqparse.add_argument('X-SESSION-ID', type = str, required = True, location='headers', dest='session_id')

#Authentication wrapper, checks if a valid session_id is provided
def authentication_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        session_id = auth_reqparse.parse_args()['session_id']

        #TODO: check whether the session id is valid by retrieving user_id from CommonSense
        user_id = commonsense.get_user_id(session_id)
        if user_id is None:
            respond(e_invalid_session)

        g._session_id = session_id

        return f(*args, **kwargs)

    return decorated_function


app_key_reqparse = reqparse.RequestParser()
app_key_reqparse.add_argument('X-APPLICATION-KEY', type = str, required = True, location='headers', dest='app_key')

#Application verification wrapper. Checks if the application key is valid
def application_verification(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        app_key = app_key_reqparse.parse_args()['app_key']

        application_key = Application_Key.query(key=app_key)

        if not application_key:
            respond(e_invalid_app_key)

        application = application_key[0].application_id

        g._application = application

        return f(*args, **kwargs)

    return decorated_function
