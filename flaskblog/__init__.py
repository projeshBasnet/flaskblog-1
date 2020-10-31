from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)
mail = Mail(app)
app.config['SECRET_KEY'] = '56d26325a50a35f667c6'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///main.db'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
app.config['MAIL-SERVER']='smtp.gmail.com'
app.config['MAIL-PORT']= 587
app.config['MAIL-USE-TLS']= True
app.config['MAIL-USERNAME']= os.environ.get('EMAIL-USER')
app.config['MAIL-PASS']= os.environ.get('EMAIL-PASS')


login_manager.login_view= 'users.login'
login_manager.login_message_category= 'info'

from flaskblog.user.routes import users
from flaskblog.post.routes import posts
from flaskblog.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)