from app import db

class Availability(db.Model):
    """Doctor availability schedule model"""
    __tablename__ = 'availability'
    
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0=Monday, 6=Sunday
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    
    __table_args__ = (
        db.Index('idx_doctor_day', 'doctor_id', 'day_of_week'),
    )
    
    def __repr__(self):
        return f'<Availability Doctor:{self.doctor_id} Day:{self.day_of_week}>'
