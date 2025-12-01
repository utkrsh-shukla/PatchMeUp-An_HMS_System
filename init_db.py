import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import create_app, db
from app.models import User, Department

def init_database():
    app = create_app()
    with app.app_context():
        print("Creating database tables...")
        db.drop_all()
        db.create_all()
        print("✓ Database tables created successfully!")
        
        print("\nCreating default admin user...")
        admin = User(email='admin@hospital.com', role='admin', is_active=True)
        admin.set_password('admin123')
        db.session.add(admin)
        print("✓ Admin user created (email: admin@hospital.com, password: admin123)")
        
        print("\nCreating sample departments...")
        departments = [Department(name='Cardiology', description='Heart and cardiovascular system care'),
                      Department(name='Neurology', description='Brain and nervous system care'),
                      Department(name='Orthopedics', description='Bone, joint, and muscle care'),
                      Department(name='Pediatrics', description='Children healthcare services'),
                      Department(name='General Medicine', description='General health and wellness'),
                      Department(name='Dermatology', description='Skin and hair care'),
                      Department(name='Oncology', description='Cancer treatment and care')]
        
        for dept in departments:
            db.session.add(dept)
            print(f"  - {dept.name}")
        
        db.session.commit()
        print("\n✓ Database initialized successfully!")
        print("\n" + "=" * 60)
        print("DEFAULT ADMIN CREDENTIALS:")
        print("Email: admin@hospital.com")
        print("Password: admin123")
        print("=" * 60)
        print("\nTo start the application, run: python run.py")

if __name__ == '__main__':
    init_database()
