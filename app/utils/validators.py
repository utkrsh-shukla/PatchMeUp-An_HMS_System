from wtforms.validators import ValidationError
from app.models.appointment import Appointment
from app.models.availability import Availability
from datetime import datetime, date

def validate_active_doctor(form, field):
    """Validate that the selected doctor is active"""
    if hasattr(form, 'doctor_id'):
        from app.models.doctor import Doctor
        
        doctor_id = form.doctor_id.data if hasattr(form.doctor_id, 'data') else form.doctor_id
        
        if doctor_id:
            doctor = Doctor.query.get(doctor_id)
            if not doctor or not doctor.user.is_active:
                raise ValidationError('This doctor is currently unavailable for appointments.')

def validate_appointment_conflict(form, field):
    doctor_id = None
    if hasattr(form, 'doctor_id'):
        doctor_id = form.doctor_id.data if hasattr(form.doctor_id, 'data') else form.doctor_id
    elif hasattr(form, 'doctor_id'):
        doctor_id = getattr(form, 'doctor_id', None)
    
    if doctor_id and hasattr(form, 'date'):
        appointment_date = form.date.data
        appointment_time = field.data
        appointment_id = getattr(form, 'appointment_id', None)
        
        query = Appointment.query.filter_by(
            doctor_id=doctor_id, date=appointment_date, time=appointment_time
        ).filter(Appointment.status.in_(['booked', 'rescheduled']))
        
        if appointment_id:
            query = query.filter(Appointment.id != appointment_id)
        
        if query.first():
            raise ValidationError('This time slot is already booked.')

def validate_doctor_availability(form, field):
    doctor_id = None
    if hasattr(form, 'doctor_id'):
        doctor_id = form.doctor_id.data if hasattr(form.doctor_id, 'data') else form.doctor_id
    elif hasattr(form, 'doctor_id'):
        doctor_id = getattr(form, 'doctor_id', None)
    
    if doctor_id and hasattr(form, 'date'):
        from app.models.doctor import Doctor
        
        appointment_date = form.date.data
        appointment_time = field.data
        
        if not doctor_id or not appointment_date or not appointment_time:
            return
        
        doctor = Doctor.query.get(doctor_id)
        if not doctor or not doctor.user.is_active:
            raise ValidationError('This doctor is currently unavailable for appointments.')
        
        day_of_week = appointment_date.weekday()
        availability_slots = Availability.query.filter_by(
            doctor_id=doctor_id, day_of_week=day_of_week, is_available=True
        ).all()
        
        if not availability_slots:
            raise ValidationError('Doctor is not available on this day.')
        
        is_within_slot = any(slot.start_time <= appointment_time < slot.end_time for slot in availability_slots)
        
        if not is_within_slot:
            raise ValidationError('Doctor is not available at this time. Please check the doctor\'s availability schedule.')

def validate_future_date(form, field):
    if field.data and field.data < date.today():
        raise ValidationError('Appointment date must be in the future.')

def validate_future_datetime(form, field):
    if hasattr(form, 'date') and hasattr(form, 'time'):
        appointment_date = form.date.data
        appointment_time = field.data
        
        if appointment_date and appointment_time:
            appointment_datetime = datetime.combine(appointment_date, appointment_time)
            if appointment_datetime < datetime.now():
                raise ValidationError('Appointment must be scheduled for a future time.')
