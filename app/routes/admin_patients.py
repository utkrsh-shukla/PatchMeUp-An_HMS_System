from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app.decorators import admin_required
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.forms.patient_forms import ProfileUpdateForm
from app import db

admin_patients_bp = Blueprint('admin_patients', __name__)

@admin_patients_bp.route('/patients')
@login_required
@admin_required
def list_patients():
    return render_template('admin/patients.html', patients=Patient.query.all())

@admin_patients_bp.route('/patients/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_patient(id):
    patient = Patient.query.get_or_404(id)
    form = ProfileUpdateForm(obj=patient)
    
    if form.validate_on_submit():
        patient.name = form.name.data
        patient.phone = form.phone.data
        patient.date_of_birth = form.date_of_birth.data
        patient.address = form.address.data
        patient.blood_group = form.blood_group.data or None
        patient.medical_history = form.medical_history.data
        
        db.session.commit()
        flash(f'Patient {patient.name} updated successfully!', 'success')
        return redirect(url_for('admin_patients.list_patients'))
    
    return render_template('admin/patient_form.html', form=form, title='Edit Patient', patient=patient)

@admin_patients_bp.route('/patients/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    patient_name = patient.name
    
    # Delete the patient record (this will also delete the user due to cascade)
    db.session.delete(patient)
    db.session.delete(patient.user)
    db.session.commit()
    
    flash(f'Patient {patient_name} has been permanently deleted.', 'success')
    return redirect(url_for('admin_patients.list_patients'))

@admin_patients_bp.route('/patients/<int:id>/deactivate', methods=['POST'])
@login_required
@admin_required
def deactivate_patient(id):
    patient = Patient.query.get_or_404(id)
    patient.user.is_active = False
    db.session.commit()
    flash(f'Patient {patient.name} has been deactivated.', 'info')
    return redirect(url_for('admin_patients.list_patients'))

@admin_patients_bp.route('/patients/<int:id>/history')
@login_required
@admin_required
def patient_history(id):
    patient = Patient.query.get_or_404(id)
    appointments = Appointment.query.filter_by(patient_id=patient.id).order_by(Appointment.date.desc()).all()
    return render_template('admin/patient_history.html', patient=patient, appointments=appointments)
