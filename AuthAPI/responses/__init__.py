from flask import make_response
from flask.ext.restful import abort

s_created       = {"msg": "", "code": 201}
s_no_content    = {"msg": "", "code": 204}

e_unauthorized          = {"msg": "unauthorized!", "code": 403}
e_missing_properties    = {"msg": "missing properties!", "code": 400}
e_conflict              = {"msg": "database operation failed!", "code": 409}
e_user_exists           = {"msg": "user with that email address exists!", "code": 409}
e_no_session            = {"msg": "no session_id provided!", "code": 401}
e_invalid_session       = {"msg": "invalid session_id!", "code": 401}
e_user_not_found        = {"msg": "user does not exist!", "code": 403}
e_sensor_not_found      = {"msg": "sensor does not exist!", "code": 403}
e_user_application      = {"msg": "user doesn't use this application", "code": 403}
e_no_app_key            = {"msg": "no application key provided!", "code": 401}
e_invalid_app_key       = {"msg": "invalid application key", "code": 401}

e_internal_error        = {"msg": "internal error!", "code": 500}
e_bad_gateway           = {"msg": "interaction with focuscura failed!", "code": 502}

def respond(response):
    abort(response["code"], message=response["msg"])