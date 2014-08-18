import senseapi
from flask import g
from .. import app
import json
from ..responses import respond

_config = None

def set_config(server, verbosity):
    global _config
    _config =   {   'server':           server,
                    'verbosity':        verbosity,
                }

def _get_sense_api():
    api = senseapi.SenseAPI()
    api.setServer(_config['server'])
    api.setVerbosity(_config['verbosity'])
    return api

def get_user_id(session_id):
    api = _get_sense_api()
    api.SetSessionId(session_id)
    if not api.UsersGetCurrent():
        return None, api.getError()
    else:
        user_id = json.loads(api.getResponse())['user']['id']
        return user_id, None

def login_user(username, password):
    api = _get_sense_api()

    if not api.AuthenticateSessionId(username, password):
        return None, api.getError()
    else:
        session_id = api.getResponse()
        return session_id, None

def create_user(email, password):
    api = _get_sense_api()

    user = {"user": {"email": email, "username": email, "password": password}}

    # attempt to create the user in CommonSense
    if not api.CreateUser(user):
        app.logger.error("Creating user failed!".format(user_id))
        return None, api.getError()
    else:
        user_id = json.loads(api.getResponse())['user']['id']
        return user_id, None

def delete_user(user_id, session_id = None, username = None, password = None):
    api = _get_sense_api()

    if not session_id is None:
        api.SetSessionId(session_id)
    elif not (username is None or password is None):
        api.AuthenticateSessionId(username, password)
    else:
        return False

    if not api.UsersDelete(user_id):
        app.logger.error("Deleting user {0} failed!".format(user_id))
        return None, api.getError()
    else:
        return None, None

def change_password(user_id, session_id = None, username = None, password = None, new_password = None):
    api = _get_sense_api()

    if not session_id is None:
        api.SetSessionId(session_id)
    elif not (username is None or password is None):
        api.AuthenticateSessionId(username, password)
    else:
        return False

    if not api.UsersChangePassword(password, new_password):
        app.logger.error("Changing Password for user {0} failed!".format(user_id))
        return None, api.getError()
    else:
        return None, None

def create_sensor(session_id, name, display_name, device_type, data_type, data_structure):
    api = _get_sense_api()

    parameters = api.SensorsPost_Parameters()
    sensor = parameters['sensor']
    sensor['name'] = name
    sensor['display_name'] = display_name
    sensor['device_type'] = device_type
    sensor['data_type'] = data_type
    if data_structure:
        sensor['data_structure'] = json.dumps(data_structure)

    api.SetSessionId(session_id)

    if not api.SensorsPost(parameters):
        app.logger.error("Create new sensors failed")
        return None, api.getError()
    else:
        sensor_id = json.loads(api.getResponse())['sensor']['id']
        return sensor_id, None

def delete_sensor(session_id, sensor_id):
    api = _get_sense_api()

    api.SetSessionId(session_id)

    if not api.SensorsDelete(sensor_id):
        app.logger.error("Delete sensors failed")
        return None, api.getError()
    else:
        return None, None

def create_metatags(session_id, sensor_id, new_metatags):
    api = _get_sense_api()

    api.SetSessionId(session_id)

    data = {"metatags": new_metatags}
    if not api.SensorMetatagsPost(sensor_id, data):
        app.logger.error("Update sensor metatags failed")
        return None, api.getError()
    else:
        return None, None

def find_sensor_by_metatags(session_id, metatags):
    api = _get_sense_api()

    api.SetSessionId(session_id)

    parameters = {"details" : "no"}
    filters =  {"filter": {"metatag_statement_groups": metatags }}

    print filters
    if not api.SensorsFind(parameters=parameters, filters=filters):
        app.logger.error("Failed to search sensors with metatags")
        return None, api.getError()
    else:
        sensors_id = json.loads(api.getResponse())['sensors']
        return sensors_id, None

def post_sensor_data(session_id, sensor_id, sensor_data):
    api = _get_sense_api()

    api.SetSessionId(session_id)

    # current commonsense cannot store data in pure json, have to be a string
    if isinstance(sensor_data['value'], dict):
        sensor_data['value'] = "\""+json.dumps(sensor_data['value'])+"\""

    if not api.SensorDataPost(sensor_id, {"data": [sensor_data]}):
        app.logger.error("Failed to upload data")
        return None, api.getError()
    else:
        return None, None

def get_sensor_data(session_id, sensors_id, start_time = None, end_time = None, sort = None, limit = None):
    api = _get_sense_api()

    api.SetSessionId(session_id)

    parameters = api.SensorDataGet_Parameters()

    if start_time:
        parameters["start_date"] = start_time
    if end_time:
        parameters["end_date"] = end_time
    if sort:
        parameters["sort"] = sort
    if limit:
        parameters['per_page'] = limit

    if not api.SensorsDataGet(sensors_id, parameters):
        app.logger.error("Failed to retrieve data")
        print api.getError()
        return None, api.getError()
    else:
        sensors_data = json.loads(api.getResponse())["data"]

        for sensor_data in sensors_data:
            data_value = sensor_data["value"]
            # chek if data is number
            try:
                data_value = float(data_value)
            except:
                # check if data is stored as json
                try:
                    data_value = json.loads(data_value[1:-1])
                except:
                    pass
            sensor_data["value"] = data_value
        
        return sensors_data, None

def delete_sensor_data(session_id, sensor_id, data_id):
    api = _get_sense_api()

    api.SetSessionId(session_id)

    if not api.SensorDataDelete(sensor_id, data_id):
        app.logger.error("Failed to delete data")
        return None, api.getError()
    else:
        return None, None
