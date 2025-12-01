from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.decorators import doctor_required
from app.models.doctor import Doctor
from app.models.availability import Availability
from app.forms.doctor_forms import AvailabilityForm
from app.utils.helpers import get_day_name
from app import db

doctor_availability_bp = Blueprint('doctor_availability', __name__)

@doctor_availability_bp.route('/availability')
@login_required
@doctor_required
def view_availability():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first_or_404()
    availability_records = Availability.query.filter_by(doctor_id=doctor.id).order_by(
        Availability.day_of_week
    ).all()
    
    weekly_schedule = {}
    for record in availability_records:
        day = record.day_of_week
        if day not in weekly_schedule:
            weekly_schedule[day] = []
        weekly_schedule[day].append(record)
    
    return render_template('doctor/availability.html',
                         doctor=doctor, weekly_schedule=weekly_schedule, get_day_name=get_day_name)

@doctor_availability_bp.route('/availability/add', methods=['GET', 'POST'])
@login_required
@doctor_required
def add_availability():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first_or_404()
    form = AvailabilityForm()
    
    if form.validate_on_submit():
        availability = Availability(
            doctor_id=doctor.id, day_of_week=form.day_of_week.data,
            start_time=form.start_time.data, end_time=form.end_time.data,
            is_available=form.is_available.data
        )
        db.session.add(availability)
        db.session.commit()
        flash('Availability updated successfully!', 'success')
        return redirect(url_for('doctor_availability.view_availability'))
    
    return render_template('doctor/availability_form.html', form=form)

@doctor_availability_bp.route('/availability/<int:id>/delete', methods=['POST'])
@login_required
@doctor_required
def delete_availability(id):
    availability = Availability.query.get_or_404(id)
    doctor = Doctor.query.filter_by(user_id=current_user.id).first_or_404()
    
    if availability.doctor_id != doctor.id:
        flash('Unauthorized access.', 'danger')
    else:
        db.session.delete(availability)
        db.session.commit()
        flash('Availability slot removed.', 'info')
    
    return redirect(url_for('doctor_availability.view_availability'))
