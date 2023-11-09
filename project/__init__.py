# init.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 

from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://ion:admin@127.0.0.1:1521/ORCLCDB'

    db.init_app(app)
    
    bootstrap = Bootstrap5(app)
    csrf = CSRFProtect(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth_blueprint.login'
    login_manager.init_app(app)

    from .models import Dmuser

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return db.session.query(Dmuser).get(int(user_id))

    # blueprints:
    with app.app_context(): # idk, w/o app_context I get a RuntimmeError
        from .auth import auth_blueprint
        from .main import main_blueprint
        from .profile import profile_blueprint

        app.register_blueprint(auth_blueprint)
        app.register_blueprint(main_blueprint)
        app.register_blueprint(profile_blueprint)

    return app