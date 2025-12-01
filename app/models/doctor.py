from app import db

class Doctor(db.Model):
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    phone = db.Column(db.String(20))
    years_of_experience = db.Column(db.Integer, default=0)
    
    appointments = db.relationship('Appointment', backref='doctor', lazy='dynamic', cascade='all, delete-orphan')
    availability = db.relationship('Availability', backref='doctor', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Doctor {self.name}>'
