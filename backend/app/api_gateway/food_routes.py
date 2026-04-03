from app import app, db
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload
import app.ai_service as ais
from app.db_models import FoodListing, User
from datetime import datetime
import uuid
import json
import logging

logger = logging.getLogger(__name__)

@app.route('/api/food/add', methods=['POST'])
@jwt_required()
def add_food():
    """Add a new food listing.
    
    BUG FIX: Now reads from request JSON instead of hardcoded data
    BUG FIX: Now requires JWT authentication
    BUG FIX: Stores to database instead of returning mock data
    """
    try:
        donor_id = get_jwt_identity()
        
        # Verify donor exists
        donor = User.query.filter_by(uid=donor_id).first()
        if not donor:
            return jsonify({"message": "Donor user not found"}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({"message": "Request body must be JSON"}), 400
        
        # Validate required fields
        required_fields = ['title', 'food_type', 'quantity', 'quantity_unit', 'expiry_date']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"message": f"Missing required field: {field}"}), 400
        
        # Validate food type
        valid_food_types = ['prepared', 'raw', 'packaged', 'baked']
        if data['food_type'] not in valid_food_types:
            return jsonify({"message": f"Invalid food_type. Must be one of: {', '.join(valid_food_types)}"}), 400
        
        # Validate quantity unit
        valid_units = ['kg', 'g', 'units', 'liters']
        if data['quantity_unit'] not in valid_units:
            return jsonify({"message": f"Invalid quantity_unit. Must be one of: {', '.join(valid_units)}"}), 400
        
        # Parse dates
        try:
            preparation_date = datetime.fromisoformat(data.get('preparation_date', datetime.now().isoformat()))
            expiry_date = datetime.fromisoformat(data['expiry_date'])
        except ValueError:
            return jsonify({"message": "Invalid date format. Use ISO 8601 format (YYYY-MM-DDTHH:MM:SS)"}), 400
        
        # Calculate freshness score
        freshness_score = ais.calculate_freshness_score(preparation_date)
        
        # Parse location if provided
        location = None
        if data.get('location'):
            try:
                location = json.dumps(data['location'])
            except TypeError:
                return jsonify({"message": "Invalid location format"}), 400
        
        # Create food listing
        food_listing = FoodListing(
            fid=str(uuid.uuid4()),
            donor_id=donor_id,
            title=data['title'],
            description=data.get('description', ''),
            food_type=data['food_type'],
            quantity=float(data['quantity']),
            quantity_unit=data['quantity_unit'],
            preparation_date=preparation_date,
            expiry_date=expiry_date,
            location=location,
            status='AVAILABLE'
        )
        
        db.session.add(food_listing)
        db.session.commit()
        
        return jsonify({
            "message": "Food item added successfully",
            "data": {
                "fid": food_listing.fid,
                "title": food_listing.title,
                "food_type": food_listing.food_type,
                "quantity": food_listing.quantity,
                "quantity_unit": food_listing.quantity_unit,
                "preparation_date": food_listing.preparation_date.isoformat(),
                "expiry_date": food_listing.expiry_date.isoformat(),
                "status": food_listing.status
            },
            "freshness_score": freshness_score
        }), 201
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding food: {str(e)}", exc_info=True)
        return jsonify({"message": "Failed to add food item. Please try again."}), 500


@app.route('/api/food', methods=['GET'])
@jwt_required()
def get_food_listings():
    """Get all available food listings or filter by status."""
    try:
        status = request.args.get('status', 'AVAILABLE')
        
        # Validate status
        valid_statuses = ['AVAILABLE', 'MATCHED', 'PICKED_UP', 'DELIVERED', 'EXPIRED']
        if status not in valid_statuses:
            return jsonify({"message": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}), 400
        
        listings = FoodListing.query.options(
            joinedload(FoodListing.donor)
        ).filter_by(status=status).all()
        
        return jsonify({
            "message": "Food listings retrieved",
            "count": len(listings),
            "data": [
                {
                    "fid": listing.fid,
                    "title": listing.title,
                    "food_type": listing.food_type,
                    "quantity": listing.quantity,
                    "quantity_unit": listing.quantity_unit,
                    "preparation_date": listing.preparation_date.isoformat() if listing.preparation_date else None,
                    "expiry_date": listing.expiry_date.isoformat(),
                    "status": listing.status,
                    "donor": {
                        "uid": listing.donor.uid,
                        "name": listing.donor.name,
                        "email": listing.donor.email,
                        "phone": listing.donor.phone
                    }
                }
                for listing in listings
            ]
        }), 200
    
    except Exception as e:
        return jsonify({"message": f"Error retrieving listings: {str(e)}"}), 500


@app.route('/api/food/<fid>', methods=['GET'])
@jwt_required()
def get_food_by_id(fid):
    """Get a specific food listing by ID."""
    try:
        listing = FoodListing.query.options(
            joinedload(FoodListing.donor)
        ).filter_by(fid=fid).first()
        
        if not listing:
            return jsonify({"message": "Food listing not found"}), 404
        
        return jsonify({
            "message": "Food listing retrieved",
            "data": {
                "fid": listing.fid,
                "title": listing.title,
                "description": listing.description,
                "food_type": listing.food_type,
                "quantity": listing.quantity,
                "quantity_unit": listing.quantity_unit,
                "preparation_date": listing.preparation_date.isoformat() if listing.preparation_date else None,
                "expiry_date": listing.expiry_date.isoformat(),
                "status": listing.status,
                "location": json.loads(listing.location) if listing.location else None,
                "donor": {
                    "uid": listing.donor.uid,
                    "name": listing.donor.name,
                    "email": listing.donor.email,
                    "phone": listing.donor.phone
                }
            }
        }), 200
    
    except Exception as e:
        return jsonify({"message": f"Error retrieving listing: {str(e)}"}), 500


@app.route('/api/food/<fid>', methods=['PUT'])
@jwt_required()
def update_food(fid):
    """Update a food listing."""
    try:
        user_id = get_jwt_identity()
        listing = FoodListing.query.filter_by(fid=fid).first()
        
        if not listing:
            return jsonify({"message": "Food listing not found"}), 404
        
        # Only donor can update their listing
        if listing.donor_id != user_id:
            return jsonify({"message": "Unauthorized. Only the donor can update this listing"}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({"message": "Request body must be JSON"}), 400
        
        # Update allowed fields
        if 'title' in data:
            listing.title = data['title']
        if 'description' in data:
            listing.description = data['description']
        if 'status' in data:
            valid_statuses = ['AVAILABLE', 'MATCHED', 'PICKED_UP', 'DELIVERED', 'EXPIRED']
            if data['status'] not in valid_statuses:
                return jsonify({"message": f"Invalid status"}), 400
            listing.status = data['status']
        if 'quantity' in data:
            listing.quantity = float(data['quantity'])
        
        listing.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            "message": "Food listing updated successfully",
            "data": {
                "fid": listing.fid,
                "title": listing.title,
                "status": listing.status
            }
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error updating listing: {str(e)}"}), 500


@app.route('/api/food/<fid>', methods=['DELETE'])
@jwt_required()
def delete_food(fid):
    """Delete a food listing."""
    try:
        user_id = get_jwt_identity()
        listing = FoodListing.query.filter_by(fid=fid).first()
        
        if not listing:
            return jsonify({"message": "Food listing not found"}), 404
        
        # Only donor can delete their listing
        if listing.donor_id != user_id:
            return jsonify({"message": "Unauthorized. Only the donor can delete this listing"}), 403
        
        db.session.delete(listing)
        db.session.commit()
        
        return jsonify({"message": "Food listing deleted successfully"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error deleting listing: {str(e)}"}), 500
