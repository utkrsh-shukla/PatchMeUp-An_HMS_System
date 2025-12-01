from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app.decorators import admin_required
from app.models.user import User
from app.models.doctor import Doctor
from app.models.department import Department
from app.models.availability import Availability
from app.forms.admin_forms import DoctorForm
from app import db
from datetime import time

admin_doctors_bp = Blueprint('admin_doctors', __name__)

@admin_doctors_bp.route('/doctors')
@login_required
@admin_required
def list_doctors():
    return render_template('admin/doctors.html', doctors=Doctor.query.all())

@admin_doctors_bp.route('/doctors/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_doctor():
    form = DoctorForm(is_edit=False)
    form.department_id.choices = [(d.id, d.name) for d in Department.query.all()]
    
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('admin_doctors.add_doctor'))
        
        user = User(email=form.email.data, role='doctor')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()
        
        doctor = Doctor(user_id=user.id, name=form.name.data, specialization=form.specialization.data,
                       department_id=form.department_id.data, phone=form.phone.data,
                       years_of_experience=form.years_of_experience.data or 0)
        db.session.add(doctor)
        db.session.flush()
        
        for day in range(5):
            db.session.add(Availability(doctor_id=doctor.id, day_of_week=day,
                                      start_time=time(9, 0), end_time=time(17, 0), is_available=True))
        
        db.session.commit()
        flash(f'Doctor {doctor.name} added successfully!', 'success')
        return redirect(url_for('admin_doctors.list_doctors'))
    
    return render_template('admin/doctor_form.html', form=form, title='Add Doctor')

@admin_doctors_bp.route('/doctors/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    form = DoctorForm(is_edit=True)
    form.department_id.choices = [(d.id, d.name) for d in Department.query.all()]
    
    if not form.validate_on_submit():
        form.name.data = doctor.name
        form.email.data = doctor.user.email
        form.specialization.data = doctor.specialization
        form.department_id.data = doctor.department_id
        form.phone.data = doctor.phone
        form.years_of_experience.data = doctor.years_of_experience
    
    if form.validate_on_submit():
        if form.email.data != doctor.user.email:
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash('Email already registered.', 'danger')
                return render_template('admin/doctor_form.html', form=form, title='Edit Doctor', doctor=doctor)
            doctor.user.email = form.email.data
        
        doctor.name = form.name.data
        doctor.specialization = form.specialization.data
        doctor.department_id = form.department_id.data
        doctor.phone = form.phone.data
        doctor.years_of_experience = form.years_of_experience.data or 0
        
        if form.password.data:
            doctor.user.set_password(form.password.data)
        
        db.session.commit()
        flash(f'Doctor {doctor.name} updated successfully!', 'success')
        return redirect(url_for('admin_doctors.list_doctors'))
    
    return render_template('admin/doctor_form.html', form=form, title='Edit Doctor', doctor=doctor)

@admin_doctors_bp.route('/doctors/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    doctor_name = doctor.name
    Availability.query.filter_by(doctor_id=doctor.id).delete()
    db.session.delete(doctor)
    db.session.delete(doctor.user)
    db.session.commit()
    flash(f'Doctor {doctor_name} has been permanently deleted.', 'success')
    return redirect(url_for('admin_doctors.list_doctors'))

@admin_doctors_bp.route('/doctors/<int:id>/deactivate', methods=['POST'])
@login_required
@admin_required
def deactivate_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    doctor.user.is_active = False
    db.session.commit()
    flash(f'Doctor {doctor.name} has been deactivated.', 'info')
    return redirect(url_for('admin_doctors.list_doctors'))
