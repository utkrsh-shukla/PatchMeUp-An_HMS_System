from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    from app.models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from app.routes import (auth_bp, admin_dashboard_bp, admin_doctors_bp, admin_patients_bp, admin_search_bp, 
                           doctor_dashboard_bp, doctor_appointments_bp, doctor_availability_bp,
                           patient_dashboard_bp, patient_appointments_bp, patient_profile_bp)
    
    blueprints = [(auth_bp, None), (admin_dashboard_bp, '/admin'), (admin_doctors_bp, '/admin'),
                  (admin_patients_bp, '/admin'), (admin_search_bp, '/admin'), (doctor_dashboard_bp, '/doctor'),
                  (doctor_appointments_bp, '/doctor'), (doctor_availability_bp, '/doctor'), 
                  (patient_dashboard_bp, '/patient'), (patient_appointments_bp, '/patient'), (patient_profile_bp, '/patient')]
    
    for bp, prefix in blueprints:
        app.register_blueprint(bp, url_prefix=prefix)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app
