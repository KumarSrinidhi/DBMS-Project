from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mobile = StringField('Mobile', validators=[DataRequired(), Length(min=10, max=10)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class PropertyForm(FlaskForm):
    address = TextAreaField('Address', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    carpetArea = IntegerField('Carpet Area (sq ft)', validators=[DataRequired()])
    typeId = SelectField('Property Type', coerce=int, validators=[DataRequired()])
    locationId = SelectField('Location', coerce=int, validators=[DataRequired()])
    reraRegistered = BooleanField('RERA Registered')
    furnishingType = SelectField('Furnishing Type', choices=[
        ('Unfurnished', 'Unfurnished'),
        ('Semi-Furnished', 'Semi-Furnished'),
        ('Fully Furnished', 'Fully Furnished')
    ])
    propertyAge = SelectField('Property Age', choices=[
        ('New', 'New'),
        ('1-5 years', '1-5 years'),
        ('5-10 years', '5-10 years'),
        ('10+ years', '10+ years')
    ])
    ownershipType = SelectField('Ownership Type', choices=[
        ('Freehold', 'Freehold'),
        ('Leasehold', 'Leasehold')
    ])
    listingType = SelectField('Listing Type', choices=[
        ('Buy', 'Buy'),
        ('Sell', 'Sell'),
        ('Rent', 'Rent'),
        ('New Projects', 'New Projects')
    ])
    propertyCategory = SelectField('Property Category', choices=[
        ('Residential', 'Residential'),
        ('Commercial', 'Commercial'),
        ('Agricultural', 'Agricultural')
    ])
    submit = SubmitField('List Property')