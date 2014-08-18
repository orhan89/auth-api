import MySQLdb as mdb
from flask import g
from .. import app

_config = None

def set_config(host, username, password, database):
    global _config
    _config = { 'host':     host,
                'username': username,
                'password': password,
                'database': database    }

def _connect_to_database():
    db = mdb.connect(   _config['host'],
                        _config['username'],
                        _config['password'],
                        _config['database'] )
    return db

def get_mysql_db():
    db = g.get('_database', None)
    if db is None:
        db = g._database = _connect_to_database()
    return db

@app.teardown_appcontext
def close_mysql_db(exception):
    db = g.get('_database', None)
    if db is not None:
        db.close()
