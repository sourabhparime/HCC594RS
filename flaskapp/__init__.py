# imports
from flask import Flask
import os, props


def create_app(test_config=None):
    # init app
    app = Flask(__name__, instance_relative_config=True)

    # setup db
    app.config['SQLALCHEMY_DATABASE_URI'] = props.SQLALCHEMY_DATABASE_URI
    app.secret_key = 'dev'

    if test_config is None:
        # load available instance
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # check for instance folder
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass

    # test app
    #@app.route('/hello')
    #def hello():
    #   return 'Hello World'


    from . import db
    db.init_app(app)

    return app
