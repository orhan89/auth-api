from flask import Flask

app = Flask(__name__)

from controllers import *
from views import *

def configure_app(config_file):
    app.config.from_pyfile(config_file)

    mysql_db.set_config(    app.config['DB_HOST'],
                            app.config['DB_USERNAME'],
                            app.config['DB_PASSWORD'],
                            app.config['DB_DATABASE']  )

    commonsense.set_config( app.config['CS_SERVER'],
                            app.config['CS_VERBOSITY'],
                          )

    # Setup logging
    if not app.config['DEBUG']:
        import logging
        from logging.handlers import SMTPHandler

        # log everything >= DEBUG to a file
        file_handler = logging.FileHandler("/var/log/AuthAPI/tma-api.log")
        file_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(file_handler)

        # log errors by email
        email_handler = SMTPHandler(    '127.0.0.1',
                                        "ADMIN_EMAIL",
                                        app.config['ADMINS'],
                                        "Exception in AuthAPI")
        email_handler.setLevel(logging.ERROR)
        app.logger.addHandler(email_handler)

configure_app('/etc/AuthAPI/production.cfg')
