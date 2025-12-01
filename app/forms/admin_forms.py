from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange, ValidationError

class DoctorForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Optional(), Length(min=6)])
    specialization = StringField('Specialization', validators=[DataRequired(), Length(max=100)])
    department_id = SelectField('Department', coerce=int, validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    years_of_experience = IntegerField('Years of Experience', validators=[Optional(), NumberRange(min=0, max=70)])
    submit = SubmitField('Save Doctor')
    
    def __init__(self, *args, **kwargs):
        self.is_edit = kwargs.pop('is_edit', False)
        super(DoctorForm, self).__init__(*args, **kwargs)
        if not self.is_edit:
            self.password.validators = [DataRequired(), Length(min=6)]
    
    def validate_password(self, field):
        if not self.is_edit and not field.data:
            raise ValidationError('Password is required for new doctors.')

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired(), Length(min=2)])
    search_type = SelectField('Search In', choices=[('all', 'All'), ('patients', 'Patients'), ('doctors', 'Doctors')], validators=[Optional()])
    submit = SubmitField('Search')
