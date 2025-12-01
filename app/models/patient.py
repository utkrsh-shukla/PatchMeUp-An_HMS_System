from app import db

class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.Text)
    blood_group = db.Column(db.String(5))
    medical_history = db.Column(db.Text)
    
    appointments = db.relationship('Appointment', backref='patient', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Patient {self.name}>'
