from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class UserRole(db.Model):
    __tablename__ = 'UserRole'
    roleId = db.Column(db.Integer, primary_key=True)
    roleName = db.Column(db.String(50), unique=True, nullable=False)

class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    userId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True)
    mobile = db.Column(db.String(10), unique=True)
    roleId = db.Column(db.Integer, db.ForeignKey('UserRole.roleId'), nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    createdAt = db.Column(db.DateTime, server_default=db.func.now())
    updatedAt = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    role = db.relationship('UserRole', backref='users')
    
    def get_id(self):
        return str(self.userId)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

class PropertyType(db.Model):
    __tablename__ = 'PropertyType'
    typeId = db.Column(db.Integer, primary_key=True)
    typeName = db.Column(db.String(30), unique=True, nullable=False)

class IndianLocation(db.Model):
    __tablename__ = 'IndianLocation'
    locationId = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(30), nullable=False)
    state = db.Column(db.String(30), nullable=False)
    pincode = db.Column(db.String(6))
    reraZone = db.Column(db.String(50))

class Property(db.Model):
    __tablename__ = 'Property'
    propertyId = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.Text, nullable=False)
    ownerId = db.Column(db.Integer, db.ForeignKey('Users.userId'), nullable=False)
    price = db.Column(db.Numeric(12, 2), nullable=False)
    carpetArea = db.Column(db.Integer, nullable=False)
    typeId = db.Column(db.Integer, db.ForeignKey('PropertyType.typeId'), nullable=False)
    locationId = db.Column(db.Integer, db.ForeignKey('IndianLocation.locationId'), nullable=False)
    reraRegistered = db.Column(db.Boolean, default=False)
    isActive = db.Column(db.Boolean, default=True)
    createdAt = db.Column(db.DateTime, server_default=db.func.now())
    furnishingType = db.Column(db.Enum('Unfurnished', 'Semi-Furnished', 'Fully Furnished'), default='Unfurnished')
    propertyAge = db.Column(db.String(20), default='New')
    ownershipType = db.Column(db.Enum('Freehold', 'Leasehold'), default='Freehold')
    listingType = db.Column(db.Enum('Buy', 'Sell', 'Rent', 'New Projects'), default='Sell')
    propertyCategory = db.Column(db.Enum('Residential', 'Commercial', 'Agricultural'), default='Residential')
    
    owner = db.relationship('User', backref='properties')
    property_type = db.relationship('PropertyType', backref='properties')
    location = db.relationship('IndianLocation', backref='properties')
    
    def to_dict(self):
        return {
            'id': self.propertyId,
            'type': self.property_type.typeName,
            'price': float(self.price),
            'city': self.location.city,
            'area': self.carpetArea,
            'bedrooms': getattr(self, 'residential_property', None) and getattr(self.residential_property, 'bedrooms', None),
        }

class PropertyImages(db.Model):
    __tablename__ = 'PropertyImages'
    imageId = db.Column(db.Integer, primary_key=True)
    propertyId = db.Column(db.Integer, db.ForeignKey('Property.propertyId'), nullable=False)
    imageURL = db.Column(db.String(255), nullable=False)
    isPrimary = db.Column(db.Boolean, default=False)
    
    property = db.relationship('Property', backref='images')

class UserDocument(db.Model):
    __tablename__ = 'UserDocuments'
    doc_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.userId'))
    doc_type = db.Column(db.String(50))  # 'aadhaar', 'pan', 'agreement'
    file_path = db.Column(db.String(255))
    uploaded_at = db.Column(db.DateTime, default=db.func.now())
    is_verified = db.Column(db.Boolean, default=False)
    
    user = db.relationship('User', backref='documents')




# Add other models similarly...