"""
Database models for the DreamHome Real Estate Portal.
Defines the schema and relationships between database tables using SQLAlchemy ORM.
"""
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

# Initialize SQLAlchemy instance
db = SQLAlchemy()

# Role constants for better maintainability
class Roles:
    ADMIN = 1
    AGENT = 2
    BUYER = 3
    SELLER = 4
    
    @classmethod
    def get_name(cls, role_id):
        names = {
            cls.ADMIN: 'Admin',
            cls.AGENT: 'Agent',
            cls.BUYER: 'Buyer',
            cls.SELLER: 'Seller'
        }
        return names.get(role_id, 'Unknown')

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
    isBanned = db.Column(db.Boolean, default=False)
    loginAttempts = db.Column(db.Integer, default=0)
    lastLoginAttempt = db.Column(db.DateTime)
    lastPasswordChange = db.Column(db.DateTime)
    passwordResetToken = db.Column(db.String(100), unique=True)
    passwordResetExpires = db.Column(db.DateTime)
    lastLogin = db.Column(db.DateTime)
    lastLoginIP = db.Column(db.String(45))
    createdAt = db.Column(db.DateTime, server_default=db.func.now())
    updatedAt = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    twoFactorEnabled = db.Column(db.Boolean, default=False)
    twoFactorSecret = db.Column(db.String(32))
    
    role = db.relationship('UserRole', backref='users')
    
    def get_id(self):
        return str(self.userId)
    
    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
    
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

class PropertyAmenity(db.Model):
    __tablename__ = 'PropertyAmenities'
    propertyId = db.Column(db.Integer, db.ForeignKey('Property.propertyId'), primary_key=True)
    amenityId = db.Column(db.Integer, db.ForeignKey('Amenities.amenityId'), primary_key=True)
    
    # Add relationship to Amenities
    amenity = db.relationship('Amenity', backref='properties')

class Amenity(db.Model):
    __tablename__ = 'Amenities'
    amenityId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)

class Property(db.Model):
    __tablename__ = 'Property'
    propertyId = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    maintenanceCharge = db.Column(db.Numeric(10, 2), nullable=True)
    totalFloors = db.Column(db.Integer, nullable=True)
    floorNumber = db.Column(db.Integer, nullable=True)
    waterSupply = db.Column(db.Enum('24/7', 'Fixed Time', 'Borewell', 'Municipal'), nullable=True)
    facing = db.Column(db.Enum('North', 'South', 'East', 'West', 'North-East', 'North-West', 'South-East', 'South-West'), nullable=True)
    overlooking = db.Column(db.String(100), nullable=True)
    powerBackup = db.Column(db.Enum('None', 'Partial', 'Full'), default='None')
    description = db.Column(db.Text, nullable=True)
    isFeatured = db.Column(db.Boolean, default=False)
    
    owner = db.relationship('User', backref='properties')
    property_type = db.relationship('PropertyType', backref='properties')
    location = db.relationship('IndianLocation', backref='properties')
    
    # Define a more explicit relationship with back_populates instead of backrefs
    images = db.relationship('PropertyImages', 
                           back_populates='property_rel',
                           lazy='select',
                           cascade='all, delete-orphan',
                           order_by='PropertyImages.imageId')
    
    # Add relationship to amenities
    amenities = db.relationship('PropertyAmenity', backref='property', lazy='dynamic')
    
    def to_dict(self):
        amenities_list = [{'name': pa.amenity.name, 'description': pa.amenity.description} 
                         for pa in self.amenities]
        return {
            'id': self.propertyId,
            'type': self.property_type.typeName,
            'price': float(self.price),
            'city': self.location.city,
            'state': self.location.state,
            'area': self.carpetArea,
            'furnishing': self.furnishingType,
            'age': self.propertyAge,
            'listing_type': self.listingType,
            'amenities': amenities_list,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'address': self.address,
            'rera_registered': self.reraRegistered,
            'ownership_type': self.ownershipType
        }

class PropertyImages(db.Model):
    __tablename__ = 'PropertyImages'
    imageId = db.Column(db.Integer, primary_key=True)
    propertyId = db.Column(db.Integer, db.ForeignKey('Property.propertyId'), nullable=False)
    imageURL = db.Column(db.String(255), nullable=False)
    isPrimary = db.Column(db.Boolean, default=False)
    
    # Use back_populates for the relationship
    property_rel = db.relationship('Property', back_populates='images')

class UserDocument(db.Model):
    __tablename__ = 'UserDocuments'
    doc_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.userId'))
    doc_type = db.Column(db.String(50))  # 'identity', 'address', 'income', 'property', 'legal', 'financial'
    file_path = db.Column(db.String(255))
    original_filename = db.Column(db.String(255))
    file_size = db.Column(db.Integer)  # Size in bytes
    mime_type = db.Column(db.String(100))
    upload_date = db.Column(db.DateTime, default=db.func.now())
    uploaded_at = db.Column(db.DateTime, default=db.func.now())  # Legacy field kept for backward compatibility
    is_verified = db.Column(db.Boolean, default=False)
    verified_by = db.Column(db.Integer, db.ForeignKey('Users.userId'), nullable=True)
    verification_date = db.Column(db.DateTime, nullable=True)
    rejection_reason = db.Column(db.String(500), nullable=True)
    
    # Define relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='documents')
    verified_by_user = db.relationship('User', foreign_keys=[verified_by], backref='verified_documents')




# Add other models similarly...