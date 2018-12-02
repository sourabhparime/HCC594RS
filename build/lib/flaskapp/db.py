from flask_sqlalchemy import SQLAlchemy
import click, props
from flask import current_app, g
from flask.cli import with_appcontext
from odo import odo, drop
from flaskapp import recommender



def get_db():

    if 'db' not in g:
        current_app.config['SQLALCHEMY_DATABASE_URI'] = props.SQLALCHEMY_DATABASE_URI
        db = SQLAlchemy(current_app)
        g.db = db
        return g.db
    else:
        return g.db


def get_similar(user_id):
    db = get_db()
    results = db.session.execute("Select * from similar_users where user_handle="+str(user_id))
    close_db()

    return results

def get_int(user_id):
    db = get_db()
    results = db.session.execute("Select * from user_interests where user_handle="+str(user_id))
    close_db()
    return results

def get_views(user_id):
    db = get_db()
    results = db.session.execute("Select * from user_course_views where user_handle="+str(user_id))
    close_db()
    return results

def get_levels(user_id):
    db = get_db()
    results = db.session.execute("Select * from user_course_views where user_handle="+str(user_id))
    close_db()
    return results


def push_to_db():
    db = get_db()

    for table_name in db.engine.table_names():

        print(table_name)
        db.engine.execute("DROP TABLE IF EXISTS "+table_name+";")

    #drop(props.USER_VIEWS_URI)
    #drop(props.COURSE_TAGS_URI)
    #drop(props.USER_ASSES_URI)
    #drop(props.USER_INTERESTS_URI)
    odo(props.USER_VIEWS, props.USER_VIEWS_URI)
    odo(props.USER_ASSES, props.USER_ASSES_URI)
    odo(props.USER_INTERESTS, props.USER_INTERESTS_URI)
    odo(props.COURSE_TAGS, props.COURSE_TAGS_URI)
    calculate_similar()
    odo(props.SIMILARITY, props.SIMILARITY_URI)


def calculate_similar():
    recommender.create_recommender_matrix()



@click.command('push_to_db')
@with_appcontext
def push_to_db_command():
    """Clear the existing data and create new tables."""
    push_to_db()
    #calculate_similar()
    click.echo('Initialized the database.')

def close_db(e=None):
    db = get_db()

    if db is not None:
        db.delete
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(push_to_db_command)
