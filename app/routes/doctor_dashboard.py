from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.decorators import doctor_required
from app.models.doctor import Doctor
from app.models.appointment import Appointment
from datetime import date

doctor_dashboard_bp = Blueprint('doctor_dashboard', __name__)

@doctor_dashboard_bp.route('/dashboard')
@login_required
@doctor_required
def index():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first_or_404()
    
    upcoming_appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.date >= date.today(),
        Appointment.status.in_(['booked', 'rescheduled'])
    ).order_by(Appointment.date, Appointment.time).all()
    
    today_appointments = [apt for apt in upcoming_appointments if apt.date == date.today()]
    
    stats = {
        'total_appointments': Appointment.query.filter_by(doctor_id=doctor.id).count(),
        'completed': Appointment.query.filter_by(doctor_id=doctor.id, status='completed').count(),
        'pending': Appointment.query.filter(
            Appointment.doctor_id == doctor.id,
            Appointment.status.in_(['booked', 'rescheduled'])
        ).count()
    }
    
    return render_template('doctor/dashboard.html',
                         doctor=doctor, upcoming_appointments=upcoming_appointments,
                         today_appointments=today_appointments, **stats)
