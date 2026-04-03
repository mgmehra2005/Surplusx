from app import app
from flask import request, jsonify
import app.ai_service as ais
from datetime import datetime
from app.api_gateway.auth_routes import token_required


@app.route('/api/food/add', methods=['POST'])
@token_required
def add_food(current_user):
    """
    {
    "title": "Fresh baked goods",
    "description": "Assorted breads and pastries",
    "foodType": "baked",
    "quantity": 25,
    "quantityUnit": "kg",
    "preparationDate": "2024-01-15T10:00:00Z",
    "expiryDate": "2024-01-16T10:00:00Z",
    "location": {
        "address": "123 Bakery St",
        "city": "San Francisco",
        "state": "CA",
        "zipCode": "94103",
    }
    }
    """
    # preparation_time = "2026-03-30T15:50:00"
    # data = {
    #     "name": request.form.get('name'),
    #     # "description": request.form.get('description'),
    #     # "quantity": request.form.get('quantity'),
    #     "expiry_date": preparation_time
    # }
    # freshness_score = ais.calculate_freshness_score(preparation_time)

    if current_user != 'DONOR':
        return jsonify({"message": "Unauthorized: Only donors can add food items", "currentUser": current_user}), 403
    
    data = request.get_json()
    donor_data = {"title" : data.get('title'),
    "description" : data.get('description'),
    "foodType" : data.get('foodType'),
    "quantity" : data.get('quantity'),
    "quantityUnit" : data.get('quantityUnit'),
    "preparationDate" : data.get('preparationDate'),
    "expiryDate" : data.get('expiryDate'),
    "location" : data.get('location')}

    return jsonify({"message": "Food item added successfully", "data": data}), 201

