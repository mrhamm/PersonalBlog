from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_mail import Mail
from website.config import Config
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
import os.path as op
import os
from dotenv import load_dotenv
from flask_admin.contrib.fileadmin import FileAdmin
from elasticsearch import Elasticsearch
import time
from website.search import add_to_index
from datetime import datetime



class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated



load_dotenv()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["MAIL_SERVER"] = os.getenv('MAIL_SERVER')
app.config["MAIL_PORT"]=  587
app.config["MAIL_USE_TLS"] = True 
app.config["MAIL_USERNAME"] = os.getenv("EMAIL_ADDRESS")
app.config["MAIL_PASSWORD"] = os.getenv("EMAIL_PASSWORD")
app.config['ELASTICSEARCH_URL'] = os.getenv("ELASTICSEARCH_URL")
app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']])


db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
mail = Mail(app)


admin = Admin(app, index_view=MyAdminIndexView())
from website.models import User, Post
admin.add_view(MyModelView(User,db.session))
admin.add_view(MyModelView(Post,db.session))
path = op.join(op.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))
from website import routes

