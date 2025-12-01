from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, TimeField, SelectField, BooleanField
from wtforms.validators import DataRequired, Optional

class TreatmentForm(FlaskForm):
    diagnosis = TextAreaField('Diagnosis', validators=[DataRequired()])
    prescription = TextAreaField('Prescription', validators=[Optional()])
    notes = TextAreaField('Additional Notes', validators=[Optional()])
    submit = SubmitField('Save Treatment')

class AvailabilityForm(FlaskForm):
    day_of_week = SelectField('Day of Week', coerce=int, choices=[
        (0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), 
        (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')
    ], validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    is_available = BooleanField('Available')
    submit = SubmitField('Update Availability')
