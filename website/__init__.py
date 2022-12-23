from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_Name = "database.db"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "lkjsdf324a234ac234sajdk9sad2"  # Use to secret you login session and your website date
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_Name}"
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    
    from .models import User, Note

    #  Best way from create_database method
    with app.app_context():
        db.create_all()
        
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

# def create_database(app):
#     if not path.exists('website/'+ DB_Name):
#         db.create_all(app=app)
#         print("Created Database!")
