from flask import Blueprint, render_template
from flask_login import login_required
from app.decorators import admin_required
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.appointment import Appointment
from datetime import date

admin_dashboard_bp = Blueprint('admin_dashboard', __name__)

@admin_dashboard_bp.route('/dashboard')
@login_required
@admin_required
def index():
    stats = {
        'total_doctors': Doctor.query.count(),
        'total_patients': Patient.query.count(),
        'total_appointments': Appointment.query.count(),
        'recent_doctors': Doctor.query.order_by(Doctor.id.desc()).limit(5).all(),
        'recent_patients': Patient.query.order_by(Patient.id.desc()).limit(5).all(),
        'upcoming_appointments': Appointment.query.filter(
            Appointment.date >= date.today(),
            Appointment.status.in_(['booked', 'rescheduled'])
        ).order_by(Appointment.date, Appointment.time).limit(10).all(),
        'booked_count': Appointment.query.filter_by(status='booked').count(),
        'completed_count': Appointment.query.filter_by(status='completed').count(),
        'cancelled_count': Appointment.query.filter_by(status='cancelled').count()
    }
    
    return render_template('admin/dashboard.html', **stats)

@admin_dashboard_bp.route('/appointments')
@login_required
@admin_required
def appointments():
    appointments = Appointment.query.order_by(Appointment.date.desc(), Appointment.time.desc()).all()
    return render_template('admin/appointments.html', appointments=appointments)
