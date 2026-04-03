# 🔄 BEFORE & AFTER - ALL FIXES

## Fix #1: health_routes.py - Text Wrapper

### ❌ BEFORE (Line 37)
```python
@app.route('/api/status', methods=['GET'])
def status():
    """Get detailed system status information."""
    try:
        db.session.execute('SELECT 1')  # ❌ Missing text() wrapper
        
        return jsonify({
            "status": "running",
            ...
        }), 200
```

### ✅ AFTER
```python
from sqlalchemy import text  # Added import

@app.route('/api/status', methods=['GET'])
def status():
    """Get detailed system status information."""
    try:
        db.session.execute(text('SELECT 1'))  # ✅ Fixed with text()
        
        return jsonify({
            "status": "running",
            ...
        }), 200
```

---

## Fix #2: auth_routes.py - JWT Token Response

### ❌ BEFORE (Line 20)
```python
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if "@" in username:
        login_status = loginWithEmail(username, password)
        if login_status:
            return jsonify({
                "message": "Login successful with email!", 
                "role": _getUserRoleByEmail(username)
                # ❌ NO TOKEN RETURNED!
            }), 200
```

### ✅ AFTER
```python
from flask_jwt_extended import create_access_token  # Added import

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login with username or email.
    
    BUG FIX: Now returns JWT token in response
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "Request body is required"}), 400
    
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({"message": "Username/email and password are required"}), 400
    
    if "@" in username:
        login_status = loginWithEmail(username, password)
        if login_status:
            role = _getUserRoleByEmail(username)
            token = create_access_token(identity=username)  # ✅ Generate token
            return jsonify({
                "message": "Login successful with email!",
                "token": token,  # ✅ Include token
                "username": username,
                "email": username,
                "role": role
            }), 200
```

---

## Fix #3: food_routes.py - Complete Rewrite

### ❌ BEFORE (Only 1 endpoint)
```python
from app import app, db
from flask import request, jsonify
import app.ai_service as ais
from app.db_models import FoodListing, User

@app.route('/api/food/add', methods=['POST'])
def add_food():
    preparation_time = "2026-03-30T15:50:00"  # ❌ HARDCODED DATE!
    data = {
        "name": request.form.get('name'),
        "expiry_date": preparation_time
    }
    freshness_score = ais.calculate_freshness_score(preparation_time)
    return jsonify({
        "message": "Food item added successfully", 
        "data": data, 
        "freshness_score": freshness_score
    }), 201

# ❌ Missing GET, PUT, DELETE endpoints!
```

### ✅ AFTER (5 complete endpoints)
```python
from app import app, db
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import text
import app.ai_service as ais
from app.db_models import FoodListing, User
from app.utils import sanitize_input
from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)

VALID_FOOD_TYPES = ['prepared', 'raw', 'packaged', 'baked']
VALID_QUANTITY_UNITS = ['kg', 'g', 'units', 'liters']
VALID_STATUSES = ['AVAILABLE', 'MATCHED', 'PICKED_UP', 'DELIVERED', 'EXPIRED']

# ✅ ENDPOINT #1: GET ALL FOODS
@app.route('/api/food', methods=['GET'])
def get_foods():
    """Get all available food items with optional filtering.
    
    Query Parameters:
    - status: Filter by status
    - food_type: Filter by food type
    - donor_id: Filter by donor
    - limit: Limit results (default 50)
    - offset: Offset for pagination (default 0)
    """
    try:
        status = request.args.get('status', 'AVAILABLE')
        food_type = request.args.get('food_type')
        donor_id = request.args.get('donor_id')
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        query = FoodListing.query
        
        if status:
            if status not in VALID_STATUSES:
                return jsonify({"message": f"Invalid status. Valid values: {VALID_STATUSES}"}), 400
            query = query.filter_by(status=status)
        
        if food_type:
            if food_type not in VALID_FOOD_TYPES:
                return jsonify({"message": f"Invalid food type. Valid types: {VALID_FOOD_TYPES}"}), 400
            query = query.filter_by(food_type=food_type)
        
        if donor_id:
            query = query.filter_by(donor_id=donor_id)
        
        total = query.count()
        foods = query.offset(offset).limit(limit).all()
        
        return jsonify({
            "message": "Food items retrieved successfully",
            "data": [food.to_dict() for food in foods],
            "pagination": {
                "total": total,
                "limit": limit,
                "offset": offset,
                "returned": len(foods)
            }
        }), 200
    except Exception as e:
        logger.error(f"Error fetching food items: {str(e)}", exc_info=True)
        return jsonify({"message": "Failed to fetch food items", "error": str(e)}), 500

# ✅ ENDPOINT #2: GET SINGLE FOOD
@app.route('/api/food/<food_id>', methods=['GET'])
def get_food(food_id):
    """Get a specific food item by ID."""
    try:
        food = FoodListing.query.filter_by(fid=food_id).first()
        
        if not food:
            return jsonify({"message": "Food item not found"}), 404
        
        return jsonify({
            "message": "Food item retrieved successfully",
            "data": food.to_dict()
        }), 200
    except Exception as e:
        logger.error(f"Error fetching food item {food_id}: {str(e)}", exc_info=True)
        return jsonify({"message": "Failed to fetch food item", "error": str(e)}), 500

# ✅ ENDPOINT #3: CREATE FOOD (Improved)
@app.route('/api/food/add', methods=['POST'])
@jwt_required()
def add_food():
    """Add a new food item - NOW USES DYNAMIC DATES"""
    try:
        user_id = get_jwt_identity()
        user = User.query.filter_by(uid=user_id).first()
        
        if not user:
            return jsonify({"message": "User not found"}), 401
        
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        required_fields = ['title', 'description', 'food_type', 'quantity', 
                          'quantity_unit', 'preparation_date', 'expiry_date']
        for field in required_fields:
            if field not in data or not str(data.get(field)).strip():
                return jsonify({"message": f"Missing required field: {field}"}), 400
        
        food_type = str(data.get('food_type')).lower()
        if food_type not in VALID_FOOD_TYPES:
            return jsonify({
                "message": f"Invalid food type. Valid types: {VALID_FOOD_TYPES}"
            }), 400
        
        quantity_unit = str(data.get('quantity_unit')).lower()
        if quantity_unit not in VALID_QUANTITY_UNITS:
            return jsonify({
                "message": f"Invalid quantity unit. Valid units: {VALID_QUANTITY_UNITS}"
            }), 400
        
        # ✅ NOW USES DYNAMIC DATES FROM REQUEST!
        try:
            prep_date = datetime.fromisoformat(str(data.get('preparation_date')).replace('Z', '+00:00'))
            expiry_date = datetime.fromisoformat(str(data.get('expiry_date')).replace('Z', '+00:00'))
        except ValueError as e:
            return jsonify({"message": f"Invalid date format. Use ISO format: {str(e)}"}), 400
        
        now = datetime.utcnow()
        if prep_date > now:
            return jsonify({"message": "Preparation date cannot be in the future"}), 400
        
        if expiry_date <= prep_date:
            return jsonify({"message": "Expiry date must be after preparation date"}), 400
        
        try:
            freshness_score = ais.calculate_freshness_score(str(data.get('expiry_date')))
        except Exception as e:
            logger.warning(f"Failed to calculate freshness score: {str(e)}")
            freshness_score = 0.5
        
        location = {}
        if isinstance(data.get('location'), dict):
            location = data.get('location')
        elif data.get('location'):
            import json
            try:
                location = json.loads(data.get('location'))
            except json.JSONDecodeError:
                location = {}
        
        food_item = FoodListing(
            fid=str(uuid.uuid4()),
            title=sanitize_input(str(data.get('title')), max_length=200),
            description=sanitize_input(str(data.get('description')), max_length=1000),
            food_type=food_type,
            quantity=float(data.get('quantity')),
            quantity_unit=quantity_unit,
            preparation_date=prep_date,
            expiry_date=expiry_date,
            location=location,
            donor_id=user_id,
            freshness_score=freshness_score,
            status='AVAILABLE'
        )
        
        db.session.add(food_item)
        db.session.commit()
        
        return jsonify({
            "message": "Food item added successfully",
            "data": food_item.to_dict(),
            "freshness_score": freshness_score
        }), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding food item: {str(e)}", exc_info=True)
        return jsonify({"message": "Failed to add food item", "error": str(e)}), 500

# ✅ ENDPOINT #4: UPDATE FOOD
@app.route('/api/food/<food_id>', methods=['PUT'])
@jwt_required()
def update_food(food_id):
    """Update a food item - with ownership validation"""
    try:
        user_id = get_jwt_identity()
        food = FoodListing.query.filter_by(fid=food_id).first()
        
        if not food:
            return jsonify({"message": "Food item not found"}), 404
        
        if food.donor_id != user_id:
            return jsonify({"message": "Unauthorized: You can only update your own listings"}), 403
        
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        # Update allowed fields with validation...
        if 'title' in data:
            food.title = sanitize_input(str(data.get('title')), max_length=200)
        
        if 'status' in data:
            status = str(data.get('status')).upper()
            if status not in VALID_STATUSES:
                return jsonify({
                    "message": f"Invalid status. Valid statuses: {VALID_STATUSES}"
                }), 400
            food.status = status
        
        food.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            "message": "Food item updated successfully",
            "data": food.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating food item {food_id}: {str(e)}", exc_info=True)
        return jsonify({"message": "Failed to update food item", "error": str(e)}), 500

# ✅ ENDPOINT #5: DELETE FOOD
@app.route('/api/food/<food_id>', methods=['DELETE'])
@jwt_required()
def delete_food(food_id):
    """Delete a food item - with ownership validation"""
    try:
        user_id = get_jwt_identity()
        food = FoodListing.query.filter_by(fid=food_id).first()
        
        if not food:
            return jsonify({"message": "Food item not found"}), 404
        
        if food.donor_id != user_id:
            return jsonify({"message": "Unauthorized: You can only delete your own listings"}), 403
        
        db.session.delete(food)
        db.session.commit()
        
        return jsonify({"message": "Food item deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting food item {food_id}: {str(e)}", exc_info=True)
        return jsonify({"message": "Failed to delete food item", "error": str(e)}), 500
```

---

## Fix #4: db_models/__init__.py - Model Enhancement

### ❌ BEFORE
```python
class FoodListing(db.Model):
    __tablename__ = 'food_listings'
    
    fid = db.Column(db.String(36), primary_key=True)
    donor_id = db.Column(db.String(36), db.ForeignKey('users.uid'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    food_type = db.Column(db.Enum('prepared', 'raw', 'packaged', 'baked'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    quantity_unit = db.Column(db.Enum('kg', 'g', 'units', 'liters'), nullable=False)
    preparation_date = db.Column(db.DateTime)
    expiry_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.JSON)
    status = db.Column(db.Enum('AVAILABLE', 'MATCHED', 'PICKED_UP', 'DELIVERED', 'EXPIRED'), default='AVAILABLE')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # ❌ NO to_dict() method
    # ❌ NO freshness_score field
```

### ✅ AFTER
```python
class FoodListing(db.Model):
    __tablename__ = 'food_listings'
    
    fid = db.Column(db.String(36), primary_key=True)
    donor_id = db.Column(db.String(36), db.ForeignKey('users.uid'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    food_type = db.Column(db.Enum('prepared', 'raw', 'packaged', 'baked'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    quantity_unit = db.Column(db.Enum('kg', 'g', 'units', 'liters'), nullable=False)
    preparation_date = db.Column(db.DateTime)
    expiry_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.JSON)
    status = db.Column(db.Enum('AVAILABLE', 'MATCHED', 'PICKED_UP', 'DELIVERED', 'EXPIRED'), default='AVAILABLE')
    freshness_score = db.Column(db.Float, default=0.0)  # ✅ Added!
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # ✅ Added to_dict() method
    def to_dict(self):
        """Convert FoodListing to dictionary for JSON serialization."""
        return {
            'id': self.fid,
            'donor_id': self.donor_id,
            'title': self.title,
            'description': self.description,
            'food_type': self.food_type,
            'quantity': self.quantity,
            'quantity_unit': self.quantity_unit,
            'preparation_date': self.preparation_date.isoformat() if self.preparation_date else None,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'location': self.location,
            'status': self.status,
            'freshness_score': self.freshness_score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
```

---

## Summary Table

| Issue | Before | After | Status |
|-------|--------|-------|--------|
| text() wrapper | ❌ Missing | ✅ Added | FIXED |
| JWT in response | ❌ None | ✅ Included | FIXED |
| Hardcoded date | ❌ "2026-03-30..." | ✅ Dynamic | FIXED |
| GET endpoint | ❌ Missing | ✅ Implemented | FIXED |
| PUT endpoint | ❌ Missing | ✅ Implemented | FIXED |
| DELETE endpoint | ❌ Missing | ✅ Implemented | FIXED |
| Validation | ❌ None | ✅ Complete | FIXED |
| Auth check | ❌ None | ✅ JWT required | FIXED |
| Ownership check | ❌ None | ✅ Verified | FIXED |
| Model method | ❌ Missing | ✅ to_dict() | FIXED |
| Freshness score | ❌ Calculated only | ✅ Stored | FIXED |

