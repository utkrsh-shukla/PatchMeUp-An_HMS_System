from app import db

class Department(db.Model):
    """Medical department/specialization model"""
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    
    # Relationships
    doctors = db.relationship('Doctor', backref='department', lazy='dynamic')
    
    def __repr__(self):
        return f'<Department {self.name}>'
