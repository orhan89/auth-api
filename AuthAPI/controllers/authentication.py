from AuthAPI.views.authentication import *
from AuthAPI import api

api.add_resource(Login, '/login')