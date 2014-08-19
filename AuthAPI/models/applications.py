from AuthAPI.services import mysql_db
from AuthAPI import app
from AuthAPI import models
import traceback

class Application(models.Model):

    model_name = 'applications'
    
    name = models.Field(default="Application Name")
    suffix = models.Field()

class Application_Key(models.Model):

	model_name = 'applications_key'

	application_id = models.ForeignField(related="applications.id")
	type = models.Field()
	key = models.Field()