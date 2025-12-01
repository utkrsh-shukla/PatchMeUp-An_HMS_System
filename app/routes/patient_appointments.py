from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.decorators import patient_required
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.appointment import Appointment
from app.models.availability import Availability
from app.forms.patient_forms import AppointmentBookingForm, AppointmentRescheduleForm
from app.utils.helpers import get_next_7_days, generate_time_slots
from app import db
from datetime import date

patient_appointments_bp = Blueprint('patient_appointments', __name__)

@patient_appointments_bp.route('/doctors/<int:id>')
@login_required
@patient_required
def doctor_detail(id):
    doctor = Doctor.query.get_or_404(id)
    
    # Check if doctor is active
    if not doctor.user.is_active:
        flash('This doctor is currently unavailable.', 'warning')
        return redirect(url_for('patient_dashboard.list_doctors'))
    
    next_days = get_next_7_days()
    availability_schedule = {
        day: Availability.query.filter_by(
            doctor_id=doctor.id, day_of_week=day.weekday(), is_available=True
        ).all() for day in next_days
    }
    
    return render_template('patient/doctor_detail.html',
                         doctor=doctor, availability_schedule=availability_schedule, next_days=next_days)

@patient_appointments_bp.route('/appointments/book/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
@patient_required
def book_appointment(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    
    # Check if doctor is active
    if not doctor.user.is_active:
        flash('This doctor is currently unavailable for appointments.', 'warning')
        return redirect(url_for('patient_dashboard.list_doctors'))
    
    patient = Patient.query.filter_by(user_id=current_user.id).first_or_404()
    
    form = AppointmentBookingForm()
    form.doctor_id.choices = [(doctor.id, doctor.name)]
    form.doctor_id.data = doctor.id
    
    if form.validate_on_submit():
        if not doctor.user.is_active:
            flash('This doctor is no longer available for appointments.', 'danger')
            return redirect(url_for('patient_dashboard.list_doctors'))
        
        # Check for appointment conflicts
        existing_appointment = Appointment.query.filter_by(
            doctor_id=doctor.id, date=form.date.data, time=form.time.data
        ).filter(Appointment.status.in_(['booked', 'rescheduled'])).first()
        
        if existing_appointment:
            flash('This time slot is already booked. Please choose another time.', 'danger')
            return render_template('patient/book_appointment.html', form=form, doctor=doctor, time_slots=generate_time_slots())
        
        try:
            appointment = Appointment(
                doctor_id=doctor.id, patient_id=patient.id,
                date=form.date.data, time=form.time.data,
                notes=form.notes.data, status='booked'
            )
            db.session.add(appointment)
            db.session.commit()
            flash('Appointment booked successfully!', 'success')
            return redirect(url_for('patient_appointments.my_appointments'))
        except Exception as e:
            db.session.rollback()
            flash('This time slot is no longer available. Please choose another time.', 'danger')
            return render_template('patient/book_appointment.html', form=form, doctor=doctor, time_slots=generate_time_slots())
    
    return render_template('patient/book_appointment.html',
                         form=form, doctor=doctor, time_slots=generate_time_slots())

@patient_appointments_bp.route('/appointments')
@login_required
@patient_required
def my_appointments():
    patient = Patient.query.filter_by(user_id=current_user.id).first_or_404()
    
    upcoming = Appointment.query.filter(
        Appointment.patient_id == patient.id,
        Appointment.date >= date.today(),
        Appointment.status.in_(['booked', 'rescheduled'])
    ).order_by(Appointment.date, Appointment.time).all()
    
    past = Appointment.query.filter(
        Appointment.patient_id == patient.id
    ).filter(
        (Appointment.date < date.today()) |
        (Appointment.status.in_(['completed', 'cancelled']))
    ).order_by(Appointment.date.desc(), Appointment.time.desc()).all()
    
    return render_template('patient/appointments.html', upcoming=upcoming, past=past)

@patient_appointments_bp.route('/appointments/<int:id>/cancel', methods=['POST'])
@login_required
@patient_required
def cancel_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    patient = Patient.query.filter_by(user_id=current_user.id).first_or_404()
    
    if appointment.patient_id != patient.id:
        flash('Unauthorized access.', 'danger')
    elif appointment.date < date.today():
        flash('Cannot cancel past appointments.', 'warning')
    else:
        appointment.status = 'cancelled'
        db.session.commit()
        flash('Appointment cancelled successfully.', 'info')
    
    return redirect(url_for('patient_appointments.my_appointments'))

@patient_appointments_bp.route('/appointments/<int:id>/reschedule', methods=['GET', 'POST'])
@login_required
@patient_required
def reschedule_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    patient = Patient.query.filter_by(user_id=current_user.id).first_or_404()
    
    if appointment.patient_id != patient.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('patient_appointments.my_appointments'))
    
    if appointment.date < date.today():
        flash('Cannot reschedule past appointments.', 'warning')
        return redirect(url_for('patient_appointments.my_appointments'))
    
    if appointment.status not in ['booked', 'rescheduled']:
        flash('Cannot reschedule this appointment.', 'warning')
        return redirect(url_for('patient_appointments.my_appointments'))
    
    form = AppointmentRescheduleForm()
    form.doctor_id = appointment.doctor_id
    form.appointment_id = appointment.id
    
    # Only populate form with original data on GET request (initial load)
    if not form.is_submitted():
        form.date.data = appointment.date
        form.time.data = appointment.time
        form.notes.data = appointment.notes
    
    if form.validate_on_submit():
        existing_appointment = Appointment.query.filter_by(
            doctor_id=appointment.doctor_id, date=form.date.data, time=form.time.data
        ).filter(Appointment.status.in_(['booked', 'rescheduled'])).filter(Appointment.id != appointment.id).first()
        
        if existing_appointment:
            flash('This time slot is already booked. Please choose another time.', 'danger')
        else:
            day_of_week = form.date.data.weekday()
            availability_slots = Availability.query.filter_by(
                doctor_id=appointment.doctor_id, day_of_week=day_of_week, is_available=True
            ).all()
            
            if not availability_slots:
                flash('Doctor is not available on this day.', 'danger')
            else:
                is_within_slot = any(slot.start_time <= form.time.data < slot.end_time for slot in availability_slots)
                if not is_within_slot:
                    flash('Doctor is not available at this time. Please check the doctor\'s availability schedule.', 'danger')
                else:
                    try:
                        appointment.date = form.date.data
                        appointment.time = form.time.data
                        appointment.notes = form.notes.data
                        appointment.status = 'rescheduled'
                        db.session.commit()
                        flash('Appointment rescheduled successfully!', 'success')
                        return redirect(url_for('patient_appointments.my_appointments'))
                    except Exception as e:
                        db.session.rollback()
                        flash('This time slot is no longer available. Please choose another time.', 'danger')
    else:
        # Debug: Show form errors if validation fails
        if form.is_submitted():
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{field}: {error}', 'danger')
    
    return render_template('patient/reschedule_appointment.html', form=form, appointment=appointment, time_slots=generate_time_slots())

@patient_appointments_bp.route('/treatments/<int:id>/view')
@login_required
@patient_required
def view_treatment(id):
    from app.models.treatment import Treatment
    treatment = Treatment.query.get_or_404(id)
    patient = Patient.query.filter_by(user_id=current_user.id).first_or_404()
    
    # Check if this treatment belongs to the current patient
    if treatment.appointment.patient_id != patient.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('patient_appointments.my_appointments'))
    
    return render_template('patient/treatment_view.html', treatment=treatment)

@patient_appointments_bp.route('/appointments/<int:id>/treatment')
@login_required
@patient_required
def view_appointment_treatment(id):
    appointment = Appointment.query.get_or_404(id)
    patient = Patient.query.filter_by(user_id=current_user.id).first_or_404()
    
    if appointment.patient_id != patient.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('patient_appointments.my_appointments'))
    
    if not appointment.treatment:
        flash('No treatment record found for this appointment.', 'info')
        return redirect(url_for('patient_appointments.my_appointments'))
    
    return redirect(url_for('patient_appointments.view_treatment', id=appointment.treatment.id))

@patient_appointments_bp.route('/medical-history')
@login_required
@patient_required
def medical_history():
    patient = Patient.query.filter_by(user_id=current_user.id).first_or_404()
    
    # Get all appointments with treatments
    appointments_with_treatments = Appointment.query.filter(
        Appointment.patient_id == patient.id,
        Appointment.treatment != None
    ).order_by(Appointment.date.desc()).all()
    
    return render_template('patient/medical_history.html', 
                         patient=patient, 
                         appointments=appointments_with_treatments)
