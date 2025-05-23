from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Property, PropertyType, IndianLocation, PropertyImages, Amenity, PropertyAmenity, UserRole, UserDocument, Roles
from config import Config
from forms import LoginForm, RegistrationForm, PropertyForm
import os
import random
from sqlalchemy import and_, or_, not_, text
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Create database tables
def init_db():
    with app.app_context():
        db.create_all()
        
        # Initialize amenities if they don't exist
        amenities = [
            {'id': 1, 'name': 'Swimming Pool', 'description': 'Swimming pool facility'},
            {'id': 2, 'name': 'Gym', 'description': 'Modern fitness center'},
            {'id': 3, 'name': 'Garden', 'description': 'Landscaped garden area'},
            {'id': 4, 'name': 'Parking', 'description': 'Reserved parking space'},
            {'id': 5, 'name': 'Security', 'description': '24/7 security service'},
            {'id': 6, 'name': 'Playground', 'description': 'Children\'s playground'}
        ]
        
        for amenity_data in amenities:
            amenity = db.session.get(Amenity, amenity_data['id'])
            if not amenity:
                amenity = Amenity(
                    amenityId=amenity_data['id'],
                    name=amenity_data['name'],
                    description=amenity_data['description']
                )
                db.session.add(amenity)
        
        # Initialize roles if they don't exist
        roles = [
            {'id': Roles.ADMIN, 'name': 'Admin'},
            {'id': Roles.AGENT, 'name': 'Agent'},
            {'id': Roles.BUYER, 'name': 'Buyer'},
            {'id': Roles.SELLER, 'name': 'Seller'}
        ]
        
        for role_data in roles:
            role = db.session.get(UserRole, role_data['id'])
            if not role:
                role = UserRole(roleId=role_data['id'], roleName=role_data['name'])
                db.session.add(role)
        
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(email='admin@realestate.com').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@realestate.com',
                mobile='9999999999',
                roleId=Roles.ADMIN  # Admin role
            )
            admin.set_password('admin123')
            db.session.add(admin)
        
        try:
            db.session.commit()
        except Exception as e:
            print(f"Error initializing database: {e}")
            db.session.rollback()

init_db()

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    if user and user.isBanned:
        return None  # Return None for banned users which will log them out
    return user

# Add before_request middleware to check ban status
@app.before_request
def check_user_ban_status():
    # Only check if user is authenticated
    if current_user.is_authenticated:
        user = User.query.get(current_user.userId)
        if user and user.isBanned:
            logout_user()
            flash('Your account has been banned. Please contact the administrator.', 'danger')
            return redirect(url_for('login'))

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    properties = Property.query.filter_by(isActive=True).limit(6).all()
    return render_template('index.html', properties=properties)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            if user.isBanned:
                flash('Your account has been banned. Please contact the administrator.', 'danger')
                return render_template('auth/login.html', form=form)
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        flash('Invalid username or password', 'danger')
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            mobile=form.mobile.data,
            roleId=Roles.BUYER  # Default role as buyer
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=form)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload/<int:property_id>', methods=['POST'])
@login_required
def upload_image(property_id):
    property = Property.query.get_or_404(property_id)
    if property.ownerId != current_user.userId and current_user.roleId != Roles.ADMIN:  # Allow owners and admins
        abort(403)
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Create property folder if it doesn't exist
            property_folder = os.path.join('static', 'images', 'properties', str(property_id))
            os.makedirs(property_folder, exist_ok=True)
            
            # Save file with secure filename
            filename = secure_filename(file.filename)
            file_path = os.path.join(property_folder, filename)
            file.save(file_path)
            
            # Store correct path in database
            image_url = f'/static/images/properties/{property_id}/{filename}'
            image = PropertyImages(
                propertyId=property_id,
                imageURL=image_url,
                isPrimary=len(property.images) == 0  # Make first image primary
            )
            db.session.add(image)
            db.session.commit()
            
            # Return success response with imageUrl for client-side handling
            return jsonify({
                'success': True,
                'imageUrl': image_url,
                'imageId': image.imageId
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/search')
def search():
    query = request.args.get('q', '')
    properties = Property.query.join(IndianLocation).filter(
        or_(
            Property.address.ilike(f'%{query}%'),
            IndianLocation.city.ilike(f'%{query}%'),
            IndianLocation.state.ilike(f'%{query}%')
        )
    ).limit(10).all()
    return render_template('search/results.html', properties=properties, query=query)

@app.route('/properties')
def properties():
    # Get filter parameters from URL
    query = Property.query.filter_by(isActive=True)

    # Basic filters
    if city := request.args.get('city'):
        query = query.join(IndianLocation).filter(IndianLocation.city.ilike(f'%{city}%'))
    if min_price := request.args.get('min_price'):
        query = query.filter(Property.price >= float(min_price))
    if max_price := request.args.get('max_price'):
        query = query.filter(Property.price <= float(max_price))
    if property_type := request.args.get('type'):
        query = query.filter(Property.typeId == int(property_type))
    if min_area := request.args.get('min_area'):
        query = query.filter(Property.carpetArea >= float(min_area))
    if max_area := request.args.get('max_area'):
        query = query.filter(Property.carpetArea <= float(max_area))
    
    # New filters
    if category := request.args.get('category'):
        query = query.filter(Property.propertyCategory == category)
    if listing_type := request.args.get('listing_type'):
        query = query.filter(Property.listingType == listing_type)
    if property_age := request.args.get('property_age'):
        query = query.filter(Property.propertyAge == property_age)
    if furnishing := request.args.get('furnishing'):
        query = query.filter(Property.furnishingType == furnishing)
    if facing := request.args.get('facing'):
        query = query.filter(Property.facing == facing)
    if water_supply := request.args.get('water_supply'):
        query = query.filter(Property.waterSupply == water_supply)
    if power_backup := request.args.get('power_backup'):
        query = query.filter(Property.powerBackup == power_backup)
    if 'rera_registered' in request.args:
        query = query.filter(Property.reraRegistered == True)
    
    # Sorting
    sort = request.args.get('sort', 'newest')
    if sort == 'price_low':
        query = query.order_by(Property.price.asc())
    elif sort == 'price_high':
        query = query.order_by(Property.price.desc())
    elif sort == 'area':
        query = query.order_by(Property.carpetArea.desc())
    else:  # newest
        query = query.order_by(Property.createdAt.desc())
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    properties = query.paginate(page=page, per_page=9)
    
    # Get filter options
    cities = db.session.query(IndianLocation.city).distinct().all()
    property_types = PropertyType.query.all()
    
    return render_template('properties/list.html', 
                         properties=properties,
                         cities=cities,
                         property_types=property_types)

@app.route('/property/<int:property_id>')
def property_detail(property_id):
    try:
        # Load property with eager loading of images
        property = Property.query.options(
            db.joinedload(Property.images)
        ).get_or_404(property_id)
        
        # Debug output to see what image paths are stored in the database
        print(f"\n-------- DEBUGGING PROPERTY {property_id} IMAGES ---------")
        if hasattr(property, 'images'):
            print(f"Property {property_id} has {len(property.images)} images:")
            for img in property.images:
                print(f"Image ID: {img.imageId}, URL in DB: {img.imageURL}")
                # Construct the filesystem path to check if image file exists
                if img.imageURL.startswith('/static/'):
                    fs_path = os.path.join(app.root_path, img.imageURL[1:])  # Remove leading slash
                else:
                    fs_path = os.path.join(app.root_path, 'static', img.imageURL)
                print(f"Looking for file at: {fs_path}")
                print(f"File exists: {os.path.exists(fs_path)}")
        else:
            print("Property has no images relationship!")
        print("-------- END DEBUG ---------\n")
        
        # Check if property is active or if the current user is admin or the property owner
        if not property.isActive:
            # Allow access if user is admin or the property owner
            if not current_user.is_authenticated or (current_user.roleId != Roles.ADMIN and property.ownerId != current_user.userId):
                flash('This property is not currently active', 'warning')
                return redirect(url_for('properties'))

        # Enhanced image handling with better error checking
        if not hasattr(property, 'images') or property.images is None:
            property.images = []
            
        # Query images directly if the relationship isn't working properly
        if len(property.images) == 0:
            images = PropertyImages.query.filter_by(propertyId=property_id).all()
            if images:
                property.images = images
                # Debug logging to diagnose image issues
                print(f"Retrieved {len(images)} images for property {property_id} directly from database")
        
        # Get amenities for this property
        amenities = []
        try:
            amenities = property.amenities
        except Exception as e:
            print(f"Error loading amenities: {str(e)}")
        
        # Add debug context to help track the issue
        debug_context = {
            'property_id': property_id,
            'image_count': len(property.images),
            'image_urls': [img.imageURL for img in property.images] if property.images else []
        }
            
        return render_template('properties/detail.html', 
                            property=property,
                            amenities=amenities,
                            debug=debug_context)
    except Exception as e:
        print(f"Error in property_detail route: {str(e)}")
        flash('An error occurred while loading the property details', 'danger')
        return redirect(url_for('properties'))

@app.route('/add-property', methods=['GET', 'POST'])
@login_required
def add_property():
    form = PropertyForm()
    if form.validate_on_submit():
        try:
            # Add validation similar to edit_property
            # Validate carpet area
            carpet_area = form.carpet_area.data
            max_area = 100000  # 100,000 sq.ft maximum
            
            if isinstance(carpet_area, str):
                carpet_area = carpet_area.replace(',', '')
                try:
                    carpet_area = float(carpet_area)
                except ValueError:
                    raise ValueError("Invalid carpet area value")
                    
            if carpet_area <= 0 or carpet_area > max_area:
                raise ValueError(f"Carpet area must be between 1 and {max_area} sq.ft")
                
            # Validate price
            price = form.price.data
            if isinstance(price, str):
                price = price.replace(',', '')
                try:
                    price = float(price)
                except ValueError:
                    raise ValueError("Invalid price value")
                    
            # Validate maintenance charge if provided
            maintenance = form.maintenance_charge.data
            if maintenance and isinstance(maintenance, str):
                maintenance = maintenance.replace(',', '')
                try:
                    maintenance = float(maintenance) if maintenance else None
                except ValueError:
                    raise ValueError("Invalid maintenance charge value")
            
            # Create new property with validated data
            property = Property(
                address=form.address.data,
                ownerId=current_user.userId,
                price=price,
                carpetArea=carpet_area,
                typeId=form.property_type.data,
                locationId=form.location.data,
                reraRegistered=form.rera_registered.data,
                furnishingType=form.furnishing_type.data,
                propertyAge=form.property_age.data,
                ownershipType=form.ownership_type.data,
                listingType=form.listing_type.data,
                propertyCategory=form.property_category.data,
                latitude=form.latitude.data,
                longitude=form.longitude.data,
                maintenanceCharge=maintenance,
                totalFloors=form.total_floors.data,
                floorNumber=form.floor_number.data,
                waterSupply=form.water_supply.data,
                facing=form.facing.data,
                overlooking=form.overlooking.data,
                powerBackup=form.power_backup.data,
                description=form.description.data
            )
            db.session.add(property)
            db.session.flush()  # Get the property ID without committing

            # Save amenities
            if form.amenities.data:
                for amenity in form.amenities.data:
                    prop_amenity = PropertyAmenity(
                        propertyId=property.propertyId,
                        amenityId=int(amenity)
                    )
                    db.session.add(prop_amenity)
            
            db.session.commit()
            flash('Your property has been listed successfully!', 'success')
            return redirect(url_for('property_detail', property_id=property.propertyId))
            
        except ValueError as e:
            db.session.rollback()
            flash(f'Validation error: {str(e)}', 'danger')
            return render_template('properties/add.html', form=form)
        except Exception as e:
            db.session.rollback()
            flash(f'Error listing property: {str(e)}', 'danger')
            return redirect(url_for('add_property'))
            
    return render_template('properties/add.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.roleId == Roles.SELLER:  # Seller
        properties = Property.query.filter_by(ownerId=current_user.userId).all()
        return render_template('dashboard/seller.html', properties=properties)
    elif current_user.roleId == Roles.BUYER:  # Buyer
        favorites = current_user.favorites
        return render_template('dashboard/buyer.html', favorites=favorites)
    elif current_user.roleId == Roles.AGENT:  # Agent
        # For now, just show all active properties since we don't have Listings
        properties = Property.query.filter_by(isActive=True).all()
        return render_template('dashboard/agent.html', properties=properties)
    else:
        return render_template('dashboard/admin.html')

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.roleId != Roles.ADMIN:  # Only for admin
        abort(403)
    
    users = User.query.all()
    properties = Property.query.all()
    return render_template('admin/dashboard.html', 
                         users=users,
                         properties=properties)

@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.roleId != Roles.ADMIN:
        abort(403)
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/properties')
@login_required
def admin_properties():
    if current_user.roleId != Roles.ADMIN:
        abort(403)
    
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Property.query
    
    if search:
        query = query.join(IndianLocation).filter(
            or_(
                Property.address.ilike(f'%{search}%'),
                IndianLocation.city.ilike(f'%{search}%'),
                IndianLocation.state.ilike(f'%{search}%')
            )
        )
    
    properties = query.paginate(
        page=page,
        per_page=10,
        error_out=False
    )
    
    return render_template('admin/properties.html',
                         properties=properties,
                         search=search)

@app.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_user(user_id):
    if current_user.roleId != Roles.ADMIN:
        abort(403)
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.mobile = request.form['mobile']
        user.roleId = int(request.form['role'])
        user.isActive = 'isActive' in request.form
        db.session.commit()
        flash('User updated successfully', 'success')
        return redirect(url_for('admin_users'))
    roles = UserRole.query.all()
    return render_template('admin/edit_user.html', user=user, roles=roles)

@app.route('/admin/edit_property/<int:property_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_property(property_id):
    if current_user.roleId != Roles.ADMIN:
        abort(403)
        
    property = Property.query.get_or_404(property_id)
    
    if request.method == 'POST':
        try:
            # Check if this is an activation/deactivation request
            if 'isActive' in request.form:
                is_active_value = request.form['isActive']
                property.isActive = is_active_value.lower() == 'true'
                db.session.commit()
                
                status = "activated" if property.isActive else "deactivated"
                flash(f'Property has been {status} successfully', 'success')
                return redirect(url_for('admin_properties'))
            
            # Otherwise, process the full form data
            if 'price' in request.form:
                property.price = float(request.form['price'])
            
            property.isActive = 'isActive' in request.form
            property.reraRegistered = 'reraRegistered' in request.form
            
            db.session.commit()
            flash('Property updated successfully', 'success')
            return redirect(url_for('admin_properties'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating property: {str(e)}', 'danger')
    
    # Get data for form dropdowns
    locations = IndianLocation.query.all()
    property_types = PropertyType.query.all()
    amenities = Amenity.query.all()
    
    # Get current property amenities
    property_amenities = [pa.amenityId for pa in property.amenities]
    
    return render_template('admin/edit_property.html',
                         property=property,
                         locations=locations,
                         property_types=property_types,
                         amenities=amenities,
                         property_amenities=property_amenities)

class Favorites(db.Model):
    __tablename__ = 'Favorites'
    userId = db.Column(db.Integer, db.ForeignKey('Users.userId'), primary_key=True)
    propertyId = db.Column(db.Integer, db.ForeignKey('Property.propertyId'), primary_key=True)
    addedAt = db.Column(db.DateTime, server_default=db.func.now())
    
    user = db.relationship('User', backref='favorites')
    property = db.relationship('Property', backref='favorited_by')

@app.route('/api/properties/search', methods=['GET'])
def advanced_search():
    filters = {
        'type_id': request.args.get('type_id'),
        'min_price': request.args.get('min_price'),
        'max_price': request.args.get('max_price'),
        'city': request.args.get('city'),
        'locality': request.args.get('locality'),
        'min_area': request.args.get('min_area'),
        'max_area': request.args.get('max_area'),
        'furnishing': request.args.get('furnishing'),
        'property_age': request.args.get('property_age'),
        'ownership': request.args.get('ownership'),
        'listing_type': request.args.get('listing_type')
    }
    
    query = Property.query.join(PropertyType).join(IndianLocation)
    
    # Apply filters
    if filters['type_id']:
        query = query.filter(Property.typeId == filters['type_id'])
    if filters['min_price']:
        query = query.filter(Property.price >= filters['min_price'])
    if filters['city']:
        query = query.filter(IndianLocation.city.ilike(f"%{filters['city']}%"))
    if filters['locality']:
        query = query.filter(Property.address.ilike(f"%{filters['locality']}%"))
    if filters['min_area']:
        query = query.filter(Property.carpetArea >= filters['min_area'])
    if filters['furnishing']:
        query = query.filter(Property.furnishingType == filters['furnishing'])
    if filters['property_age']:
        query = query.filter(Property.propertyAge == filters['property_age'])
    if filters['ownership']:
        query = query.filter(Property.ownershipType == filters['ownership'])
    if filters['listing_type']:
        query = query.filter(Property.listingType == filters['listing_type'])
    
    results = query.limit(50).all()
    return jsonify([property.to_dict() for property in results])

@app.route('/search')
def search_page():
    property_types = PropertyType.query.all()
    return render_template('search/advanced.html', property_types=property_types)

@app.route('/api/properties/search')
def search_properties():
    # Base query
    query = Property.query.filter_by(isActive=True)
    
    # Location filters
    if location := request.args.get('location'):
        query = query.join(IndianLocation).filter(
            or_(
                IndianLocation.city.ilike(f'%{location}%'),
                IndianLocation.state.ilike(f'%{location}%')
            )
        )
    
    # Price range
    if min_price := request.args.get('min_price'):
        query = query.filter(Property.price >= float(min_price))
    if max_price := request.args.get('max_price'):
        query = query.filter(Property.price <= float(max_price))
    
    # Area range
    if min_area := request.args.get('min_area'):
        query = query.filter(Property.carpetArea >= float(min_area))
    if max_area := request.args.get('max_area'):
        query = query.filter(Property.carpetArea <= float(max_area))
    
    # Property type and category
    if property_type := request.args.get('type'):
        query = query.filter(Property.typeId == int(property_type))
    if category := request.args.get('category'):
        query = query.filter(Property.propertyCategory == category)
    
    # Listing type and ownership
    if listing_type := request.args.get('listing_type'):
        query = query.filter(Property.listingType == listing_type)
    if ownership_type := request.args.get('ownership_type'):
        query = query.filter(Property.ownershipType == ownership_type)
    
    # Building details
    if min_floor := request.args.get('min_floor'):
        query = query.filter(Property.floorNumber >= int(min_floor))
    if max_floor := request.args.get('max_floor'):
        query = query.filter(Property.floorNumber <= int(max_floor))
    if facing := request.args.get('facing'):
        query = query.filter(Property.facing == facing)
    
    # Amenities
    if amenities := request.args.getlist('amenities'):
        for amenity_id in amenities:
            query = query.join(PropertyAmenity).filter(PropertyAmenity.amenityId == int(amenity_id))
    
    # Utilities
    if water_supply := request.args.get('water_supply'):
        query = query.filter(Property.waterSupply == water_supply)
    if power_backup := request.args.get('power_backup'):
        query = query.filter(Property.powerBackup == power_backup)
    
    # Age and furnishing
    if property_age := request.args.get('property_age'):
        query = query.filter(Property.propertyAge == property_age)
    if furnishing := request.args.get('furnishing'):
        query = query.filter(Property.furnishingType == furnishing)
    
    # Additional filters
    if 'rera_registered' in request.args:
        query = query.filter(Property.reraRegistered == True)
    
    # Sorting
    sort = request.args.get('sort', 'newest')
    if sort == 'price_low':
        query = query.order_by(Property.price.asc())
    elif sort == 'price_high':
        query = query.order_by(Property.price.desc())
    elif sort == 'area':
        query = query.order_by(Property.carpetArea.desc())
    else:  # newest
        query = query.order_by(Property.createdAt.desc())
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 9, type=int)
    pagination = query.paginate(page=page, per_page=per_page)
    
    # Format response
    properties = [{
        'id': p.propertyId,
        'type': p.property_type.typeName,
        'category': p.propertyCategory,
        'price': float(p.price),
        'carpet_area': p.carpetArea,
        'city': p.location.city,
        'state': p.location.state,
        'address': p.address,
        'listing_type': p.listingType,
        'furnishing': p.furnishingType,
        'age': p.propertyAge,
        'ownership': p.ownershipType,
        'rera_registered': p.reraRegistered,
        'maintenance_charge': float(p.maintenanceCharge) if p.maintenanceCharge else None,
        'total_floors': p.totalFloors,
        'floor_number': p.floorNumber,
        'water_supply': p.waterSupply,
        'facing': p.facing,
        'overlooking': p.overlooking,
        'power_backup': p.powerBackup,
        'description': p.description,
        'amenities': [{'id': pa.amenityId, 'name': pa.amenity.name} for pa in p.amenities],
        'created_at': p.createdAt.isoformat(),
        'images': [img.imageURL for img in p.images]
    } for p in pagination.items]
    
    return jsonify({
        'properties': properties,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    })

@app.route('/favorite/<int:property_id>', methods=['POST'])
@login_required
def toggle_favorite(property_id):
    favorite = Favorites.query.filter_by(
        userId=current_user.userId,
        propertyId=property_id
    ).first()

    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'status': 'removed'})
    else:
        new_fav = Favorites(
            userId=current_user.userId,
            propertyId=property_id
        )
        db.session.add(new_fav)
        db.session.commit()
        return jsonify({'status': 'added'})

@app.route('/documents/upload', methods=['POST'])
@login_required
def upload_document():
    if 'document' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['document']
    doc_type = request.form['doc_type']
    
    if file and allowed_file(file.filename):
        filename = f"user_{current_user.userId}_{doc_type}_{secure_filename(file.filename)}"
        filepath = os.path.join(app.config['DOCUMENT_UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        doc = UserDocument(
            user_id=current_user.userId,
            doc_type=doc_type,
            file_path=filepath
        )
        db.session.add(doc)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'document_id': doc.doc_id
        })
    
    return jsonify({'error': 'Invalid file'}), 400

@app.route('/tools/budget-finder')
def budget_finder():
    budget = request.args.get('budget', type=float)
    city = request.args.get('city')
    
    if budget and city:
        # Find properties within 10% of budget
        min_price = budget * 0.9
        max_price = budget * 1.1
        
        properties = Property.query.filter(
            Property.price.between(min_price, max_price),
            IndianLocation.city == city
        ).join(IndianLocation).limit(10).all()
        
        return render_template('tools/budget_results.html',
                            properties=properties,
                            budget=budget,
                            city=city)
    
    return render_template('tools/budget_finder.html')

@app.route('/property/rera-check/<int:property_id>')
def rera_check(property_id):
    property = Property.query.get_or_404(property_id)
    
    # Mock RERA verification - integrate with real API
    rera_status = {
        'is_verified': property.reraRegistered,
        'registration_number': 'RERA/' + property.location.state[:3].upper() + str(random.randint(1000, 9999)) if property.reraRegistered else None,
        'builder_details': {
            'name': 'Sample Builder' if property.reraRegistered else None,
            'license': 'RERA/' + str(random.randint(100000, 999999)) if property.reraRegistered else None
        }
    }
    
    return render_template('property/rera_status.html', 
                         property=property,
                         rera_status=rera_status)

@app.route('/loan/calculator', methods=['GET', 'POST'])
def home_loan_calculator():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        tenure = int(request.form['tenure'])
        rate = float(request.form['rate'])
        
        # EMI calculation
        monthly_rate = rate / 12 / 100
        emi = (amount * monthly_rate * (1 + monthly_rate)**tenure) / ((1 + monthly_rate)**tenure - 1)
        
        return render_template('loan/calculator.html', 
                            emi=round(emi, 2),
                            form_data=request.form)
    
    return render_template('loan/calculator.html')

@app.route('/property/valuate', methods=['POST'])
def valuate_property():
    data = request.json
    # Mock valuation algorithm - replace with real logic
    base_rate = {
        'Mumbai': 15000,
        'Bangalore': 10000,
        'Delhi': 12000
    }.get(data['city'], 8000)
    
    valuation = {
        'market_value': base_rate * int(data['area']),
        'rental_value': base_rate * int(data['area']) / 1000,
        'suggested_price_range': {
            'min': base_rate * int(data['area']) * 0.9,
            'max': base_rate * int(data['area']) * 1.1
        }
    }
    
    return jsonify(valuation)

@app.route('/loan/apply', methods=['POST'])
@login_required
def apply_loan():
    try:
        # Validate amount and convert to float
        amount = 0
        try:
            amount = float(request.form['amount'])
            if amount <= 0:
                raise ValueError("Loan amount must be greater than zero")
        except (ValueError, KeyError):
            flash("Please enter a valid loan amount", "danger")
            return redirect(url_for('loan_calculator'))
        
        # Process loan application with validation
        # Generate reference ID safely
        reference_id = f"LOAN{random.randint(100000, 999999)}"
        
        # Mock approval with safety checks
        max_amount = amount * 1.2
        
        # Create response data
        bank_response = {
            'status': 'pre_approved',
            'reference_id': reference_id,
            'max_amount': max_amount,
            'user_id': current_user.userId,
            'application_date': db.func.now()
        }
        
        return render_template('loan/application_result.html', result=bank_response)
    except Exception as e:
        flash(f"Error processing loan application: {str(e)}", "danger")
        return redirect(url_for('loan_calculator'))

@app.route('/tools/compare')
def compare_properties():
    # Get property IDs from session or query parameters - create a new list instead of directly referencing
    properties_to_compare = session.get('compare_list', [])
    if not isinstance(properties_to_compare, list):
        properties_to_compare = []
    else:
        # Create a new copy to avoid direct modification of the session object
        properties_to_compare = properties_to_compare.copy()
    
    # Handle adding new property to comparison
    if add_id := request.args.get('add'):
        add_id_int = int(add_id)
        if len(properties_to_compare) < 3 and add_id_int not in properties_to_compare:
            # Append to our copy, not directly to the session object
            properties_to_compare.append(add_id_int)
            # Then update the session with the new list
            session['compare_list'] = properties_to_compare
    
    # Handle removing property from comparison
    if remove_id := request.args.get('remove'):
        remove_id_int = int(remove_id)
        if remove_id_int in properties_to_compare:
            # Remove from our copy, not directly from the session object
            properties_to_compare.remove(remove_id_int)
            # Then update the session with the new list
            session['compare_list'] = properties_to_compare
    
    # Fetch property details for comparison
    properties = []
    if properties_to_compare:
        properties = Property.query\
            .filter(Property.propertyId.in_(properties_to_compare))\
            .all()
    
    return render_template('tools/compare.html', properties=properties)

@app.route('/tools/loan-calculator', methods=['GET', 'POST'])
def loan_calculator():
    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            tenure = int(request.form['tenure'])  # Get tenure in years
            rate = float(request.form['rate'])
            down_payment = float(request.form.get('down_payment', 0))
            
            # Calculate loan amount after down payment
            principal = amount - down_payment
            
            # Convert tenure to months for calculations
            tenure_months = tenure * 12
            
            # Monthly calculations
            monthly_rate = rate / 12 / 100
            emi = (principal * monthly_rate * (1 + monthly_rate)**tenure_months) / ((1 + monthly_rate)**tenure_months - 1)
            total_payment = emi * tenure_months
            total_interest = total_payment - principal

            # Calculate percentages
            interest_percent = (total_interest / total_payment) * 100
            principal_percent = (principal / total_payment) * 100
            
            # Calculate yearly amortization
            amortization = []
            balance = principal
            yearly_payment = emi * 12
            
            for year in range(1, tenure + 1):
                yearly_interest = 0
                yearly_principal = 0
                
                for _ in range(12):
                    monthly_interest = balance * monthly_rate
                    monthly_principal = emi - monthly_interest
                    
                    yearly_interest += monthly_interest
                    yearly_principal += monthly_principal
                    balance -= monthly_principal
                
                amortization.append({
                    'year': year,
                    'principal_paid': yearly_principal,
                    'interest_paid': yearly_interest,
                    'total_payment': yearly_principal + yearly_interest,
                    'balance': max(0, balance)  # Ensure we don't show negative balance due to rounding
                })

            return render_template('tools/loan_calculator.html', 
                                form_data={
                                    'amount': amount,
                                    'tenure': tenure,
                                    'rate': rate,
                                    'down_payment': down_payment
                                },
                                emi=emi,
                                total_payment=total_payment,
                                total_interest=total_interest,
                                interest_percent=interest_percent,
                                principal_percent=principal_percent,
                                amortization=amortization,
                                calculated=True)
        except (ValueError, ZeroDivisionError) as e:
            flash('Please enter valid numeric values for all fields', 'error')
            return render_template('tools/loan_calculator.html')
    
    return render_template('tools/loan_calculator.html')

@app.route('/tools/valuation', methods=['GET', 'POST'])
def property_valuation():
    # Fetch actual locations and amenities from database
    locations = IndianLocation.query.distinct(IndianLocation.city).all()
    amenities = Amenity.query.all()
    
    if request.method == 'POST':
        data = request.get_json()
        
        # Get valuation parameters
        carpet_area = float(data.get('carpetArea', 0))
        location_id = int(data.get('location', 0))
        property_type = data.get('propertyType', '')
        property_age = int(data.get('propertyAge', 0))
        amenities_list = data.get('amenities', [])
        
        # Base price calculation
        base_price = carpet_area * 5000  # Base rate of ₹5000 per sq ft
        
        # Location multiplier
        location = IndianLocation.query.get(location_id)
        if location:
            if location.city.lower() in ['mumbai', 'delhi']:
                base_price *= 1.8
            elif location.city.lower() in ['bangalore', 'pune', 'hyderabad']:
                base_price *= 1.5
            elif location.city.lower() in ['chennai', 'kolkata']:
                base_price *= 1.3
        
        # Property type adjustment
        type_multipliers = {
            'apartment': 1.0,
            'villa': 1.4,
            'independent': 1.2,
            'plot': 0.8
        }
        base_price *= type_multipliers.get(property_type, 1.0)
        
        # Age depreciation
        if property_age > 0:
            age_factor = max(0.6, 1 - (property_age * 0.02))  # 2% depreciation per year, minimum 60% of value
            base_price *= age_factor
        
        # Amenities bonus
        amenity_bonus = len(amenities_list) * 0.03  # 3% increase per amenity
        base_price *= (1 + amenity_bonus)
        
        # Calculate confidence score based on data completeness
        confidence_factors = [
            bool(carpet_area),
            bool(location_id),
            bool(property_type),
            bool(property_age),
            bool(amenities_list)
        ]
        confidence_score = (sum(confidence_factors) / len(confidence_factors)) * 100
        
        # Calculate range with wider spread for lower confidence
        spread_factor = (100 - confidence_score) / 100 + 0.1  # 10% minimum spread
        min_value = base_price * (1 - spread_factor)
        max_value = base_price * (1 + spread_factor)
        
        return jsonify({
            'estimated_value': round(base_price),
            'min_value': round(min_value),
            'max_value': round(max_value),
            'confidence_score': round(confidence_score),
            'location_score': 80,
            'condition_score': max(0, 100 - (property_age * 5))  # Decrease by 5% per year
        })
    
    return render_template('tools/valuation.html', 
                         locations=locations,
                         amenities=amenities)

@app.route('/about')
def about():
    return render_template('pages/about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle contact form submission
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Here you would typically send an email or save to database
        flash('Thank you for your message. We will get back to you soon!', 'success')
        return redirect(url_for('contact'))
        
    return render_template('pages/contact.html')

@app.route('/terms')
def terms():
    return render_template('pages/terms.html')

@app.route('/privacy')
def privacy():
    return render_template('pages/privacy.html')

@app.route('/admin/toggle-user-status/<int:user_id>', methods=['POST'])
@login_required
def admin_toggle_user_status(user_id):
    if current_user.roleId != Roles.ADMIN:  # Only admin can toggle user status
        abort(403)
    
    user = User.query.get_or_404(user_id)
    if user.roleId == Roles.ADMIN:  # Cannot deactivate admin users
        abort(400)
    
    user.isActive = not user.isActive
    db.session.commit()
    return jsonify({'success': True})

@app.route('/admin/toggle-property-status/<int:property_id>', methods=['POST'])
@login_required
def admin_toggle_property_status(property_id):
    if current_user.roleId != Roles.ADMIN:  # Only admin can toggle property status
        abort(403)
    
    property = Property.query.get_or_404(property_id)
    property.isActive = not property.isActive
    db.session.commit()
    return jsonify({'success': True})

@app.route('/admin/property/delete-image/<int:image_id>', methods=['POST'])
@login_required
def admin_delete_property_image(image_id):
    if current_user.roleId != Roles.ADMIN:
        abort(403)
    
    image = PropertyImages.query.get_or_404(image_id)
    try:
        # Fix path handling to be consistent with how files are saved
        # The imageURL has a leading slash that needs to be removed for filesystem path
        image_url_path = image.imageURL.lstrip('/')
        file_path = os.path.join(app.root_path, image_url_path)
        
        if os.path.exists(file_path):
            os.remove(file_path)
        
        db.session.delete(image)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/profile')
@login_required
def profile():
    if current_user.roleId == Roles.SELLER:  # Seller
        user_properties = Property.query.filter_by(ownerId=current_user.userId).all()
        return render_template('user/profile.html', user_properties=user_properties)
    elif current_user.roleId == Roles.BUYER:  # Buyer
        favorites = Favorites.query.filter_by(userId=current_user.userId).all()
        return render_template('user/profile.html', favorites=favorites)
    return render_template('user/profile.html')

@app.route('/settings')
@login_required
def settings():
    return render_template('user/settings.html')

@app.route('/settings/update-profile', methods=['POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        
        # Check if username or email already exists
        if username != current_user.username and User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('settings'))
        
        if email != current_user.email and User.query.filter_by(email=email).first():
            flash('Email already exists', 'danger')
            return redirect(url_for('settings'))
        
        current_user.username = username
        current_user.email = email
        current_user.mobile = mobile
        db.session.commit()
        
        flash('Profile updated successfully', 'success')
        return redirect(url_for('settings'))

@app.route('/settings/change-password', methods=['POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not current_user.check_password(current_password):
            flash('Current password is incorrect', 'danger')
            return redirect(url_for('settings'))
        
        if new_password != confirm_password:
            flash('New passwords do not match', 'danger')
            return redirect(url_for('settings'))
        
        current_user.set_password(new_password)
        db.session.commit()
        
        flash('Password changed successfully', 'success')
        return redirect(url_for('settings'))

@app.route('/settings/update-notifications', methods=['POST'])
@login_required
def update_notifications():
    if request.method == 'POST':
        email_notifications = 'email_notifications' in request.form
        sms_notifications = 'sms_notifications' in request.form
        marketing_emails = 'marketing_emails' in request.form
        
        # Update user preferences in database
        # This would require adding these fields to the User model
        flash('Notification preferences updated', 'success')
        return redirect(url_for('settings'))

@app.route('/settings/delete-account', methods=['POST'])
@login_required
def delete_account():
    if request.method == 'POST':
        password = request.form.get('password')
        
        if not current_user.check_password(password):
            flash('Password is incorrect', 'danger')
            return redirect(url_for('settings'))
        
        # Delete user's data
        if current_user.roleId == Roles.SELLER:  # Seller
            Property.query.filter_by(ownerId=current_user.userId).delete()
        Favorites.query.filter_by(userId=current_user.userId).delete()
        
        user_id = current_user.userId
        logout_user()
        User.query.filter_by(userId=user_id).delete()
        db.session.commit()
        
        flash('Your account has been deleted', 'info')
        return redirect(url_for('index'))

@app.route('/admin/ban-user/<int:user_id>', methods=['POST'])
@login_required
def admin_ban_user(user_id):
    if current_user.roleId != Roles.ADMIN:  # Only admin can ban users
        abort(403)
    
    user = User.query.get_or_404(user_id)
    if user.roleId == Roles.ADMIN:  # Cannot ban admin users
        flash('Cannot ban admin users', 'danger')
        return redirect(url_for('admin_users'))
    
    user.isBanned = not user.isBanned
    user.isActive = not user.isBanned  # Deactivate account if banned
    db.session.commit()
    
    action = 'banned' if user.isBanned else 'unbanned'
    flash(f'User {user.username} has been {action}', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/delete-property/<int:property_id>', methods=['POST'])
@login_required
def admin_delete_property(property_id):
    if current_user.roleId != Roles.ADMIN:  # Only admin can delete properties
        abort(403)
    
    property = Property.query.get_or_404(property_id)
    
    try:
        # 1. Delete from Favorites first (no dependencies)
        Favorites.query.filter_by(propertyId=property_id).delete()
        
        # 2. Delete Listing records (if table exists)
        try:
            db.session.execute(text("DELETE FROM Listing WHERE propertyId = :pid"), {"pid": property_id})
        except Exception as e:
            pass
        
        # 3. Delete from PropertyAmenities (no dependencies)
        PropertyAmenity.query.filter_by(propertyId=property_id).delete()
        
        # 4. Delete associated images and their files
        image_deletion_errors = []
        for image in property.images:
            try:
                file_path = os.path.join(app.root_path, image.imageURL.lstrip('/'))
                if os.path.exists(file_path):
                    os.remove(file_path)
                db.session.delete(image)
            except Exception as e:
                image_deletion_errors.append(str(e))
        
        # Handle other dependent tables - wrap each in try/except to handle if tables don't exist
        for table_name in [
            "PropertyDocuments", "Payment", "Transaction", 
            "RentalAgreement", "PropertyTax", "Maintenance",
            "Valuation", "LegalCase", "ResidentialProperty", "CommercialProperty"
        ]:
            try:
                db.session.execute(
                    text(f"DELETE FROM {table_name} WHERE propertyId = :pid"),
                    {"pid": property_id}
                )
            except Exception:
                pass
        
        # Finally delete the property itself
        db.session.delete(property)
        
        # Commit all changes
        db.session.commit()
        
        if image_deletion_errors:
            flash(f'Property deleted with warnings: Some image files could not be deleted.', 'warning')
        else:
            flash('Property has been deleted successfully', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting property: {str(e)}', 'danger')
    
    return redirect(url_for('admin_properties'))

@app.route('/admin/properties/<int:property_id>/toggle-featured', methods=['POST'])
@login_required
def admin_toggle_featured(property_id):
    if current_user.roleId != Roles.ADMIN:
        abort(403)
    
    property = Property.query.get_or_404(property_id)
    property.isFeatured = not property.isFeatured
    db.session.commit()
    
    action = 'featured' if property.isFeatured else 'unfeatured'
    flash(f'Property has been {action}', 'success')
    return redirect(url_for('admin_properties'))

@app.route('/property/<int:property_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_property(property_id):
    property = Property.query.get_or_404(property_id)
    
    # Check if user is the owner
    if property.ownerId != current_user.userId and current_user.roleId != Roles.ADMIN:
        abort(403)
        
    form = PropertyForm()
    
    if request.method == 'GET':
        # Manually populate the form with existing property data
        form.address.data = property.address
        form.price.data = property.price
        form.carpet_area.data = property.carpetArea
        form.property_type.data = property.typeId
        form.location.data = property.locationId
        form.furnishing_type.data = property.furnishingType
        form.property_age.data = property.propertyAge
        form.ownership_type.data = property.ownershipType
        form.listing_type.data = property.listingType
        form.property_category.data = property.propertyCategory
        form.rera_registered.data = property.reraRegistered
        form.latitude.data = property.latitude
        form.longitude.data = property.longitude
        form.maintenance_charge.data = property.maintenanceCharge
        form.total_floors.data = property.totalFloors
        form.floor_number.data = property.floorNumber
        form.water_supply.data = property.waterSupply
        form.facing.data = property.facing
        form.overlooking.data = property.overlooking
        form.power_backup.data = property.powerBackup
        form.description.data = property.description
        form.featured.data = property.isFeatured
        
        # Populate the amenities - get existing amenity IDs for this property
        existing_amenities = [pa.amenityId for pa in PropertyAmenity.query.filter_by(propertyId=property_id).all()]
        form.amenities.data = existing_amenities
    
    if form.validate_on_submit():
        try:
            # Get form data with validation
            carpet_area = form.carpet_area.data
            
            # Validate carpet_area: ensure it's a reasonable number for a property
            max_area = 100000  # 100,000 sq.ft is already extremely large
            
            # If carpet_area is a string (possibly with commas), clean it
            if isinstance(carpet_area, str):
                carpet_area = carpet_area.replace(',', '')
                try:
                    carpet_area = float(carpet_area)
                except ValueError:
                    raise ValueError("Invalid carpet area value")
            
            if carpet_area <= 0 or carpet_area > max_area:
                raise ValueError(f"Carpet area must be between 1 and {max_area} sq.ft")
                
            # Similar validation for price and maintenance charge
            price = form.price.data
            if isinstance(price, str):
                price = price.replace(',', '')
                try:
                    price = float(price)
                except ValueError:
                    raise ValueError("Invalid price value")
                    
            maintenance = form.maintenance_charge.data
            if maintenance and isinstance(maintenance, str):
                maintenance = maintenance.replace(',', '')
                try:
                    maintenance = float(maintenance) if maintenance else None
                except ValueError:
                    raise ValueError("Invalid maintenance charge value")
            
            # Update property with validated data
            property.address = form.address.data
            property.price = price
            property.carpetArea = carpet_area
            property.typeId = form.property_type.data
            property.locationId = form.location.data
            property.furnishingType = form.furnishing_type.data
            property.propertyAge = form.property_age.data
            property.ownershipType = form.ownership_type.data
            property.listingType = form.listing_type.data
            property.propertyCategory = form.property_category.data
            property.reraRegistered = form.rera_registered.data
            property.latitude = form.latitude.data
            property.longitude = form.longitude.data
            property.maintenanceCharge = maintenance
            property.totalFloors = form.total_floors.data
            property.floorNumber = form.floor_number.data
            property.waterSupply = form.water_supply.data
            property.facing = form.facing.data
            property.overlooking = form.overlooking.data
            property.powerBackup = form.power_backup.data
            property.description = form.description.data
            property.isFeatured = form.featured.data if form.featured else False
            
            # Update amenities
            PropertyAmenity.query.filter_by(propertyId=property_id).delete()
            if form.amenities.data:
                for amenity_id in form.amenities.data:
                    prop_amenity = PropertyAmenity(propertyId=property_id, amenityId=int(amenity_id))
                    db.session.add(prop_amenity)
            
            db.session.commit()
            flash('Property updated successfully!', 'success')
            return redirect(url_for('property_detail', property_id=property_id))
            
        except ValueError as e:
            db.session.rollback()
            flash(f'Validation error: {str(e)}', 'danger')
            return render_template('properties/add.html', form=form, edit_mode=True)
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating property: {str(e)}', 'danger')
    
    return render_template('properties/add.html', form=form, edit_mode=True)

@app.route('/property/<int:property_id>/delete', methods=['POST'])
@login_required
def delete_property(property_id):
    property = Property.query.get_or_404(property_id)
    
    # Check if user is the owner
    if property.ownerId != current_user.userId:
        abort(403)
    
    try:
        # Delete associated images first
        for image in property.images:
            try:
                file_path = os.path.join(app.root_path, image.imageURL.lstrip('/'))
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error deleting image file: {e}")
        
        # Delete property amenities
        PropertyAmenity.query.filter_by(propertyId=property_id).delete()
        
        # Delete property from favorites
        Favorites.query.filter_by(propertyId=property_id).delete()
        
        # Delete the property
        db.session.delete(property)
        db.session.commit()
        
        flash('Property has been deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting property: {str(e)}', 'danger')
    
    return redirect(url_for('dashboard'))

@app.route('/map-search')
def map_search():
    # Get all properties with coordinates
    properties = Property.query.filter(
        Property.isActive == True,
        Property.latitude.isnot(None),
        Property.longitude.isnot(None)
    ).all()
    
    # Format properties for map markers
    map_properties = [{
        'id': p.propertyId,
        'lat': p.latitude,
        'lng': p.longitude,
        'title': f"{p.property_type.typeName} in {p.location.city}",
        'price': float(p.price),
        'address': p.address,
        'area': p.carpetArea,
        'type': p.property_type.typeName,
        'category': p.propertyCategory,
        'listing_type': p.listingType,
        'image': p.images[0].imageURL if p.images else None,
        'url': url_for('property_detail', property_id=p.propertyId)
    } for p in properties]
    
    return render_template('search/map.html', 
                         properties=map_properties,
                         api_key=app.config.get('MAPS_API_KEY', ''))

if __name__ == '__main__':
    app.run(debug=True)