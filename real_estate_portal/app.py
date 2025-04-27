from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Property, PropertyType, IndianLocation, PropertyImages
from config import Config
from forms import LoginForm, RegistrationForm, PropertyForm
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

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
def loan_calculator():
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

if __name__ == '__main__':
    app.run(debug=True)