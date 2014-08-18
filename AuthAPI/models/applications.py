from AuthAPI.services import mysql_db
from AuthAPI import app
from AuthAPI import models
import traceback

class Application(models.Model):

    model_name = 'applications'
    
    app_id = models.Field
    name = models.Field
    suffix = models.Field

