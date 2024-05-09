"""init file"""
from datetime import timedelta
from flask import Flask, session,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from app.config import config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'patient.login'
login_manager.login_message_category = 'danger'

def create_app(config_name):
    """initialises app for either development or production"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    csrf = CSRFProtect(app)
    csrf.init_app(app)
    #CORS(app)


    @app.before_request
    def handle_session():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(days=1)
    

    from app.main.routes import main
    from app.patient.routes import patient
    from app.doctor.routes import doctor
    from app.admin.routes import admin
    from app.models.patient import Patient  # Import Patient model here
    from app.models.doctor import Doctor


    @login_manager.user_loader
    def load_user(user_id):
        patient = Patient.query.get(user_id)
        if patient:
            return patient
        else:
            return Doctor.query.get(user_id)

    app.register_blueprint(main)
    app.register_blueprint(patient)
    app.register_blueprint(doctor)
    app.register_blueprint(admin)

    from app.models.hospital import Hospital
    @app.context_processor
    def inject_variables():
        hospital=Hospital.query.first()
        prev_page = request.referrer
        return dict(
            hospital=hospital,
            prev_page=prev_page
        )

    return app

app = create_app('development')
