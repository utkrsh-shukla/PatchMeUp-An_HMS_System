from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.decorators import patient_required
from app.models.patient import Patient
from app.models.department import Department
from app.models.doctor import Doctor
from app.models.user import User
from app.models.appointment import Appointment
from datetime import date

patient_dashboard_bp = Blueprint('patient_dashboard', __name__)

@patient_dashboard_bp.route('/dashboard')
@login_required
@patient_required
def index():
    patient = Patient.query.filter_by(user_id=current_user.id).first_or_404()
    departments = Department.query.all()
    
    # Add active doctor count for each department
    for dept in departments:
        dept.active_doctor_count = Doctor.query.join(User, Doctor.user_id == User.id).filter(
            Doctor.department_id == dept.id,
            User.is_active == True
        ).count()
    
    upcoming_appointments = Appointment.query.filter(
        Appointment.patient_id == patient.id,
        Appointment.date >= date.today(),
        Appointment.status.in_(['booked', 'rescheduled'])
    ).order_by(Appointment.date, Appointment.time).limit(5).all()
    
    stats = {
        'total_appointments': Appointment.query.filter_by(patient_id=patient.id).count(),
        'completed': Appointment.query.filter_by(patient_id=patient.id, status='completed').count()
    }
    
    return render_template('patient/dashboard.html',
                         patient=patient, departments=departments,
                         upcoming_appointments=upcoming_appointments, **stats)

@patient_dashboard_bp.route('/doctors')
@login_required
@patient_required
def list_doctors():
    department_id = request.args.get('department', type=int)
    search_query = request.args.get('search', '').strip()
    
    # Only show active doctors
    base_query = Doctor.query.join(User, Doctor.user_id == User.id).filter(User.is_active == True)
    
    if department_id:
        base_query = base_query.filter(Doctor.department_id == department_id)
    
    if search_query:
        # Search by doctor name or specialization
        base_query = base_query.filter(
            (Doctor.name.ilike(f'%{search_query}%')) |
            (Doctor.specialization.ilike(f'%{search_query}%'))
        )
    
    doctors = base_query.all()
    departments = Department.query.all()
    
    return render_template('patient/doctors.html',
                         doctors=doctors, departments=departments, 
                         selected_department=department_id, search_query=search_query)
