"""
Contact form definition for the DreamHome Real Estate Portal.
Allows users to send inquiries, feedback, and other communications.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, Optional

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Optional(), Length(min=10, max=10)])
    subject = SelectField('Subject', choices=[
        ('', 'Select a subject'),
        ('inquiry', 'Property Inquiry'),
        ('appointment', 'Schedule Appointment'),
        ('feedback', 'Feedback'),
        ('complaint', 'Complaint'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField('Send Message')
