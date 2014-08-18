from flask import request, g, make_response
from functools import wraps, update_wrapper
from datetime import timedelta
from hashlib import sha256
import hmac
from tmaapi import app
from tmaapi.responses import *
from tmaapi.models import clients as Clients
from tmaapi.models import key as Keys
from tmaapi.services import commonsense

#Authentication wrapper, checks if a valid session_id is provided
def authentication_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        session_id = request.headers.get('X-SESSION-ID', None)
        if session_id is None:
            return respond(e_no_session)

        #TODO: check whether the session id is valid by retrieving user_id from CommonSense
        user_id = commonsense.get_user_id(session_id)
        if user_id is None:
            return respond(e_invalid_session)

        user = Clients.get_client(user_id = user_id)
        if user is None:
            return respond(e_user_not_found)

        g._session_id = session_id
        g._user = user
        return f(*args, **kwargs)

    return decorated_function


#Application verification wrapper. Checks if the application key is valid
def application_verification(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        app_key = request.headers.get('X-APP-KEY', None)
        if app_key is None:
            return respond(e_no_app_key)

        if app_key != str(app.config['APP_KEY']):
            return respond(e_invalid_app_key)

        return f(*args, **kwargs)

    return decorated_function
