from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DecimalField, IntegerField, SelectField, SelectMultipleField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from models import User, PropertyType, IndianLocation

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mobile = StringField('Mobile Number', validators=[DataRequired(), Length(min=10, max=10)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered')

    def validate_mobile(self, mobile):
        if not mobile.data.isdigit():
            raise ValidationError('Mobile number must contain only digits')
        user = User.query.filter_by(mobile=mobile.data).first()
        if user:
            raise ValidationError('Mobile number already registered')

class PropertyForm(FlaskForm):
    title = StringField('Property Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    price = DecimalField('Price (₹)', validators=[DataRequired()])
    carpet_area = IntegerField('Carpet Area (sq.ft)', validators=[DataRequired()])
    latitude = FloatField('Latitude', validators=[Optional()])
    longitude = FloatField('Longitude', validators=[Optional()])
    
    property_type = SelectField('Property Type', coerce=int, validators=[DataRequired()])
    location = SelectField('Location', coerce=int, validators=[DataRequired()])
    furnishing_type = SelectField('Furnishing Type', choices=[
        ('Unfurnished', 'Unfurnished'),
        ('Semi-Furnished', 'Semi-Furnished'),
        ('Fully Furnished', 'Fully Furnished')
    ], validators=[DataRequired()])
    
    property_age = SelectField('Property Age', choices=[
        ('New', 'New Construction'),
        ('1-5 years', '1-5 Years'),
        ('5-10 years', '5-10 Years'),
        ('10+ years', '10+ Years')
    ])
    
    ownership_type = SelectField('Ownership Type', choices=[
        ('Freehold', 'Freehold'),
        ('Leasehold', 'Leasehold')
    ])
    
    listing_type = SelectField('Listing Type', choices=[
        ('Buy', 'Buy'),
        ('Rent', 'Rent'),
        ('New Projects', 'New Projects')
    ])
    
    property_category = SelectField('Property Category', choices=[
        ('Residential', 'Residential'),
        ('Commercial', 'Commercial'),
        ('Agricultural', 'Agricultural')
    ])
    
    amenities = SelectMultipleField('Amenities', choices=[
        ('Swimming Pool', 'Swimming Pool'),
        ('Gym', 'Gym'),
        ('Garden', 'Garden'),
        ('Parking', 'Parking'),
        ('Security', 'Security'),
        ('Playground', 'Playground')
    ])
    
    rera_registered = BooleanField('RERA Registered')
    featured = BooleanField('Featured Property')
    submit = SubmitField('List Property')

    def __init__(self, *args, **kwargs):
        super(PropertyForm, self).__init__(*args, **kwargs)
        self.property_type.choices = [(t.typeId, t.typeName) for t in PropertyType.query.all()]
        self.location.choices = [(l.locationId, f"{l.city}, {l.state}") for l in IndianLocation.query.all()]

class PropertySearchForm(FlaskForm):
    location = StringField('Location')
    min_price = DecimalField('Min Price', validators=[Optional()])
    max_price = DecimalField('Max Price', validators=[Optional()])
    property_type = SelectField('Property Type', coerce=int, validators=[Optional()])
    furnishing_type = SelectField('Furnishing', choices=[
        ('', 'Any'),
        ('Unfurnished', 'Unfurnished'),
        ('Semi-Furnished', 'Semi-Furnished'),
        ('Fully Furnished', 'Fully Furnished')
    ], validators=[Optional()])
    submit = SubmitField('Search')

    def __init__(self, *args, **kwargs):
        super(PropertySearchForm, self).__init__(*args, **kwargs)
        self.property_type.choices = [(0, 'Any')] + [(t.typeId, t.typeName) for t in PropertyType.query.all()]