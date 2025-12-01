from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.decorators import doctor_required
from app.models.doctor import Doctor
from app.models.appointment import Appointment
from app.models.treatment import Treatment
from app.models.patient import Patient
from app.forms.doctor_forms import TreatmentForm
from app import db

doctor_appointments_bp = Blueprint('doctor_appointments', __name__)

@doctor_appointments_bp.route('/appointments')
@login_required
@doctor_required
def list_appointments():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first_or_404()
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).order_by(
        Appointment.date.desc(), Appointment.time.desc()
    ).all()
    return render_template('doctor/appointments.html', appointments=appointments, doctor=doctor)

@doctor_appointments_bp.route('/appointments/<int:id>/complete', methods=['POST'])
@login_required
@doctor_required
def complete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    doctor = Doctor.query.filter_by(user_id=current_user.id).first_or_404()
    
    if appointment.doctor_id != doctor.id:
        flash('Unauthorized access.', 'danger')
    else:
        appointment.status = 'completed'
        db.session.commit()
        flash('Appointment marked as completed.', 'success')
    
    return redirect(url_for('doctor_appointments.list_appointments'))

@doctor_appointments_bp.route('/appointments/<int:id>/cancel', methods=['POST'])
@login_required
@doctor_required
def cancel_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    doctor = Doctor.query.filter_by(user_id=current_user.id).first_or_404()
    
    if appointment.doctor_id != doctor.id:
        flash('Unauthorized access.', 'danger')
    else:
        appointment.status = 'cancelled'
        db.session.commit()
        flash('Appointment cancelled.', 'info')
    
    return redirect(url_for('doctor_appointments.list_appointments'))

@doctor_appointments_bp.route('/appointments/<int:id>/treatment', methods=['GET', 'POST'])
@login_required
@doctor_required
def add_treatment(id):
    appointment = Appointment.query.get_or_404(id)
    doctor = Doctor.query.filter_by(user_id=current_user.id).first_or_404()
    
    if appointment.doctor_id != doctor.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('doctor_appointments.list_appointments'))
    
    if appointment.treatment:
        flash('Treatment record already exists for this appointment.', 'warning')
        return redirect(url_for('doctor_appointments.list_appointments'))
    
    form = TreatmentForm()
    if form.validate_on_submit():
        treatment = Treatment(
            appointment_id=appointment.id, diagnosis=form.diagnosis.data,
            prescription=form.prescription.data, notes=form.notes.data
        )
        appointment.status = 'completed'
        db.session.add(treatment)
        db.session.commit()
        flash('Treatment record added successfully!', 'success')
        return redirect(url_for('doctor_appointments.list_appointments'))
    
    return render_template('doctor/treatment_form.html', form=form, appointment=appointment)

@doctor_appointments_bp.route('/treatments/<int:id>/view')
@login_required
@doctor_required
def view_treatment(id):
    treatment = Treatment.query.get_or_404(id)
    doctor = Doctor.query.filter_by(user_id=current_user.id).first_or_404()
    
    if treatment.appointment.doctor_id != doctor.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('doctor_appointments.list_appointments'))
    
    return render_template('doctor/treatment_view.html', treatment=treatment)

@doctor_appointments_bp.route('/treatments/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@doctor_required
def edit_treatment(id):
    treatment = Treatment.query.get_or_404(id)
    doctor = Doctor.query.filter_by(user_id=current_user.id).first_or_404()
    
    if treatment.appointment.doctor_id != doctor.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('doctor_appointments.list_appointments'))
    
    form = TreatmentForm(obj=treatment)
    if form.validate_on_submit():
        treatment.diagnosis = form.diagnosis.data
        treatment.prescription = form.prescription.data
        treatment.notes = form.notes.data
        db.session.commit()
        flash('Treatment record updated successfully!', 'success')
        return redirect(url_for('doctor_appointments.view_treatment', id=treatment.id))
    
    return render_template('doctor/treatment_form.html', form=form, treatment=treatment, appointment=treatment.appointment)

@doctor_appointments_bp.route('/appointments/<int:id>/treatment/edit', methods=['GET', 'POST'])
@login_required
@doctor_required
def edit_appointment_treatment(id):
    appointment = Appointment.query.get_or_404(id)
    doctor = Doctor.query.filter_by(user_id=current_user.id).first_or_404()
    
    if appointment.doctor_id != doctor.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('doctor_appointments.list_appointments'))
    
    if not appointment.treatment:
        flash('No treatment record found for this appointment.', 'warning')
        return redirect(url_for('doctor_appointments.add_treatment', id=appointment.id))
    
    return redirect(url_for('doctor_appointments.edit_treatment', id=appointment.treatment.id))

@doctor_appointments_bp.route('/patients/<int:id>/history')
@login_required
@doctor_required
def patient_history(id):
    patient = Patient.query.get_or_404(id)
    doctor = Doctor.query.filter_by(user_id=current_user.id).first_or_404()
    appointments = Appointment.query.filter_by(
        patient_id=patient.id, doctor_id=doctor.id
    ).order_by(Appointment.date.desc()).all()
    return render_template('doctor/patient_history.html', patient=patient, appointments=appointments)
