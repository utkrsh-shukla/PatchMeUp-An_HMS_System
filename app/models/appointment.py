from app import db
from datetime import datetime

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='booked')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    treatment = db.relationship('Treatment', backref='appointment', uselist=False, cascade='all, delete-orphan')
    
    __table_args__ = (
        db.Index('idx_doctor_datetime', 'doctor_id', 'date', 'time'),
        db.UniqueConstraint('doctor_id', 'date', 'time', name='uq_doctor_datetime'),
    )
    
    def __repr__(self):
        return f'<Appointment {self.id} - {self.date} {self.time}>'
