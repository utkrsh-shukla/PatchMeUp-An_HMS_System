from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.decorators import patient_required
from app.models.patient import Patient
from app.forms.patient_forms import ProfileUpdateForm
from app import db

patient_profile_bp = Blueprint('patient_profile', __name__)

@patient_profile_bp.route('/profile')
@login_required
@patient_required
def view_profile():
    patient = Patient.query.filter_by(user_id=current_user.id).first_or_404()
    return render_template('patient/profile.html', patient=patient)

@patient_profile_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
@patient_required
def edit_profile():
    patient = Patient.query.filter_by(user_id=current_user.id).first_or_404()
    form = ProfileUpdateForm(obj=patient)
    
    if form.validate_on_submit():
        patient.name = form.name.data
        patient.phone = form.phone.data
        patient.date_of_birth = form.date_of_birth.data
        patient.address = form.address.data
        patient.blood_group = form.blood_group.data or None
        patient.medical_history = form.medical_history.data
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('patient_profile.view_profile'))
    
    return render_template('patient/profile_edit.html', form=form, patient=patient)
