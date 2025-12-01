from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional, Length
from app.utils.validators import validate_appointment_conflict, validate_doctor_availability, validate_future_date, validate_active_doctor

class AppointmentBookingForm(FlaskForm):
    doctor_id = SelectField('Doctor', coerce=int, validators=[DataRequired(), validate_active_doctor])
    date = DateField('Appointment Date', validators=[DataRequired(), validate_future_date])
    time = TimeField('Appointment Time', validators=[DataRequired(), validate_doctor_availability, validate_appointment_conflict])
    notes = TextAreaField('Notes/Symptoms', validators=[Optional()])
    submit = SubmitField('Book Appointment')

class AppointmentRescheduleForm(FlaskForm):
    date = DateField('New Appointment Date', validators=[DataRequired(), validate_future_date])
    time = TimeField('New Appointment Time', validators=[DataRequired()])
    notes = TextAreaField('Notes/Symptoms', validators=[Optional()])
    submit = SubmitField('Reschedule Appointment')

class ProfileUpdateForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    date_of_birth = DateField('Date of Birth', validators=[Optional()])
    address = TextAreaField('Address', validators=[Optional()])
    blood_group = SelectField('Blood Group', choices=[('', 'Select Blood Group'), ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], validators=[Optional()])
    medical_history = TextAreaField('Medical History', validators=[Optional()])
    submit = SubmitField('Update Profile')
