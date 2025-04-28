from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Property, PropertyType, IndianLocation, PropertyImages, Amenity, PropertyAmenity
from config import Config
from forms import LoginForm, RegistrationForm, PropertyForm
import os
from sqlalchemy import and_, or_, not_

app = Flask(__name__)
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
            amenity = Amenity.query.get(amenity_data['id'])
            if not amenity:
                amenity = Amenity(
                    amenityId=amenity_data['id'],
                    name=amenity_data['name'],
                    description=amenity_data['description']
                )
                db.session.add(amenity)
        
        try:
            db.session.commit()
        except Exception as e:
            print(f"Error initializing amenities: {e}")
            db.session.rollback()

init_db()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
            roleId=3  # Default role as buyer
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=form)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload/<int:property_id>', methods=['POST'])
@login_required
def upload_image(property_id):
    property = Property.query.get_or_404(property_id)
    if property.ownerId != current_user.userId:
        abort(403)
    
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(url_for('property_detail', property_id=property_id))
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('property_detail', property_id=property_id))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(f"{property_id}_{file.filename}")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        image = PropertyImages(
            propertyId=property_id,
            imageURL=url_for('static', filename=f'uploads/{filename}'),
            isPrimary=False
        )
        db.session.add(image)
        db.session.commit()
        flash('Image uploaded successfully')
    
    return redirect(url_for('property_detail', property_id=property_id))

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
    city = request.args.get('city')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    property_type = request.args.get('type')
    
    # Start with base query
    query = Property.query.filter_by(isActive=True)
    
    # Apply filters
    if city:
        query = query.join(IndianLocation).filter(IndianLocation.city.ilike(f'%{city}%'))
    if min_price:
        query = query.filter(Property.price >= float(min_price))
    if max_price:
        query = query.filter(Property.price <= float(max_price))
    if property_type:
        query = query.filter(Property.typeId == int(property_type))
    
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
    property = Property.query.get_or_404(property_id)
    amenities = property.amenities if hasattr(property, 'amenities') else []
    return render_template('properties/detail.html', 
                         property=property,
                         amenities=amenities)

@app.route('/add-property', methods=['GET', 'POST'])
@login_required
def add_property():
    form = PropertyForm()
    if form.validate_on_submit():
        property = Property(
            address=form.address.data,
            ownerId=current_user.userId,
            price=form.price.data,
            carpetArea=form.carpetArea.data,
            typeId=form.typeId.data,
            locationId=form.locationId.data,
            reraRegistered=form.reraRegistered.data,
            furnishingType=form.furnishingType.data,
            propertyAge=form.propertyAge.data,
            ownershipType=form.ownershipType.data,
            listingType=form.listingType.data,
            propertyCategory=form.propertyCategory.data
        )
        db.session.add(property)
        db.session.commit()
        flash('Your property has been listed!', 'success')
        return redirect(url_for('property_detail', property_id=property.propertyId))
    return render_template('properties/add.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.roleId == 4:  # Seller
        properties = Property.query.filter_by(ownerId=current_user.userId).all()
        return render_template('dashboard/seller.html', properties=properties)
    elif current_user.roleId == 3:  # Buyer
        favorites = current_user.favorites
        return render_template('dashboard/buyer.html', favorites=favorites)
    elif current_user.roleId == 2:  # Agent
        listings = Listing.query.filter_by(agentId=current_user.agent.agentId).all()
        return render_template('dashboard/agent.html', listings=listings)
    else:
        return render_template('dashboard/admin.html')

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.roleId != 1:  # Only for admin
        abort(403)
    
    users = User.query.all()
    properties = Property.query.all()
    return render_template('admin/dashboard.html', 
                         users=users,
                         properties=properties)

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
        'bedrooms': request.args.get('bedrooms'),
        'bathrooms': request.args.get('bathrooms'),
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
    if filters['bedrooms'] and filters['property_category'] == 'Residential':
        query = query.join(ResidentialProperty).filter(ResidentialProperty.bedrooms >= filters['bedrooms'])
    
    # Add similar conditions for other filters
    
    results = query.limit(50).all()
    return jsonify([property.to_dict() for property in results])

@app.route('/search')
def search_page():
    property_types = PropertyType.query.all()
    return render_template('search/advanced.html', property_types=property_types)

@app.route('/api/properties/search')
def search_properties():
    # Get search parameters
    filters = []
    
    if location := request.args.get('location'):
        filters.append(or_(
            IndianLocation.city.ilike(f'%{location}%'),
            IndianLocation.state.ilike(f'%{location}%'),
            Property.address.ilike(f'%{location}%')
        ))
    
    if property_type := request.args.get('type'):
        filters.append(Property.typeId == property_type)
    
    if listing_type := request.args.get('listing_type'):
        filters.append(Property.listingType == listing_type)
    
    if min_price := request.args.get('min_price'):
        filters.append(Property.price >= float(min_price))
    
    if max_price := request.args.get('max_price'):
        filters.append(Property.price <= float(max_price))
    
    if min_area := request.args.get('min_area'):
        filters.append(Property.carpetArea >= float(min_area))
    
    if furnishing := request.args.get('furnishing'):
        filters.append(Property.furnishingType == furnishing)
    
    if property_age := request.args.get('property_age'):
        filters.append(Property.propertyAge == property_age)
    
    # Build query with joins
    query = Property.query\
        .join(PropertyType)\
        .join(IndianLocation)\
        .filter(Property.isActive == True)
    
    # Apply all filters
    if filters:
        query = query.filter(and_(*filters))
    
    # Apply sorting
    sort = request.args.get('sort', 'newest')
    if sort == 'price_low':
        query = query.order_by(Property.price.asc())
    elif sort == 'price_high':
        query = query.order_by(Property.price.desc())
    elif sort == 'area':
        query = query.order_by(Property.carpetArea.desc())
    else:  # newest
        query = query.order_by(Property.createdAt.desc())
    
    # Execute query and format results
    properties = query.all()
    results = []
    
    for property in properties:
        result = property.to_dict()
        # Check for property images, use default if none exist
        if property.images and len(property.images) > 0:
            image_url = property.images[0].imageURL
        else:
            image_url = url_for('static', filename='images/1.jpg')  # Use first default image
            
        result.update({
            'latitude': property.latitude,
            'longitude': property.longitude,
            'image_url': image_url,
            'city': property.location.city,
            'state': property.location.state,
        })
        results.append(result)
    
    return jsonify(results)

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
    # Validate and process loan application
    # Integrate with bank APIs (example with mock)
    bank_response = {
        'status': 'pre_approved',
        'reference_id': 'LOAN'+str(random.randint(100000, 999999)),
        'max_amount': request.form['amount'] * 1.2
    }
    
    return render_template('loan/application_result.html', result=bank_response)

@app.route('/tools/compare')
def compare_properties():
    # Get property IDs from session or query parameters
    properties_to_compare = session.get('compare_list', [])
    
    # Handle adding new property to comparison
    if add_id := request.args.get('add'):
        if len(properties_to_compare) < 3 and int(add_id) not in properties_to_compare:
            properties_to_compare.append(int(add_id))
            session['compare_list'] = properties_to_compare
    
    # Handle removing property from comparison
    if remove_id := request.args.get('remove'):
        if int(remove_id) in properties_to_compare:
            properties_to_compare.remove(int(remove_id))
            session['compare_list'] = properties_to_compare
    
    # Fetch property details for comparison
    properties = []
    if properties_to_compare:
        properties = Property.query\
            .filter(Property.propertyId.in_(properties_to_compare))\
            .all()
    
    return render_template('tools/compare.html', properties=properties)

@app.route('/tools/loan-calculator')
def loan_calculator():
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

if __name__ == '__main__':
    app.run(debug=True)