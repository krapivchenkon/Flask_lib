from flask import Flask,g,jsonify
import sqlite3
import logging
from logging import StreamHandler
# from werkzeug.local import LocalProxy

from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from db_setup import Base, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# engine = create_engine('sqlite:///test_user.db')
# Base.metadata.bind = engine
# 
# DBSession = sessionmaker(bind=engine)
# session = DBSession()

# @app.route('/restaurants/<int:restaurant_id>/')
# def restaurantMenu(restaurant_id):
#     restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
#     items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
#     output = ''
#     for i in items:
#         output += i.name
#         output += '</br>'
#         output += i.price
#         output += '</br>'
#         output += i.description
#         output += '</br>'
#         output += '</br>'
#     return output

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'email': self.email,
        }


# def get_db():
#     # TODO create db pool that is created on startup
#     app.logger.info("get_db called")
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = session.connect()
#     return db

@app.before_request
def before_request():
    app.logger.info("before_request called")
    # g.db = connect_db()

@app.after_request
def after_request(response):
    app.logger.info("after_request called:"+str(response))
    # g.db = connect_db()
    return response


@app.teardown_request
def teardown_req(exception):
    print "teardown_request called"
    app.logger.info("teardown_request called")

@app.teardown_appcontext
def teardown_db(exception):
    print "teardown_appcontext called"
    app.logger.info("teardown_appcontext called")
    db = getattr(g, '_database', None)
    if db is not None:
        db = 'closed'




#TODO: using flask shell
# from flask.ext.script import Shell 
# def make_shell_context():
#     return dict(app=app, db=db, User=User, Role=Role) 

# manager.add_command("shell", Shell(make_context=make_shell_context))

#TODO: add SQLAlchemy event listeners
# TODO SQLAlchemy sample without Flask-SQLAlchemy extension
# http://piotr.banaszkiewicz.org/blog/2014/02/22/how-to-bite-flask-sqlalchemy-and-pytest-all-at-once/
# TODO reusing existing Models with flask extension session object
# https://github.com/mitsuhiko/flask-sqlalchemy/issues/98
#TODO: set local proxies for this app
# db = LocalProxy(get_db)

#TODO: add testing skeleton



@app.route("/")
@app.route("/index/")
def index():

    app.logger.info("index called")
    users = User.query.all()
    app.logger.info(users)
    # import pdb; pdb.set_trace()
    # app.logger.info("connection is:"+users)
    return jsonify(Users=[user.serialize for user in users])





if __name__ == '__main__':
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")

    app.logger.handlers[0].setFormatter(formatter)
    logw = logging.getLogger('werkzeug')
    logw.setLevel(logging.DEBUG)
    logw.addHandler(app.logger.handlers[0])
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
