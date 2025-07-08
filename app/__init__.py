from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
from database.database import init_db
import os
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user



base_dir = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(base_dir, '..', 'database.db')
db = SQLAlchemy()

def create_app():



    app = Flask(__name__)
    app.config['SECRET_KEY'] = "secretkey123"  
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
    init_db()

    db.init_app(app)

    from .auth import auth
    from .views import views
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        #ici on dit a flask-login comment charger un utilisateur
        #user_id est l'id de l'utilisateur stocké dans la session
        return User.query.get(int(user_id))

    return app