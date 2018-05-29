from flask import Flask, render_template

from src.common.database import Database

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "123"  # normally is 32 characters of random letters
"""
When browser comes into app and requests a page, 
flask is going to put the cookie in them with a session id,
the session id is going to be used to link the browser to a specific session in server,
session in our server is going to contain thing like session email,
which use to verify whether a user is login or not, 
in order to secure those cookie that we gave the browser
we need a secret key
"""

@app.before_first_request
def init_db():
    Database.initialize()

@app.route('/')
def home():
    return render_template('home.html')

from src.models.users.views import user_blueprint
app.register_blueprint(user_blueprint, url_prefix="/users")
