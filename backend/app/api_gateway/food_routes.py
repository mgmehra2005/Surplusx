from app import app
from flask import request, jsonify
import app.ai_service as ais
from datetime import datetime

@app.route('/api/food/add', methods=['POST'])
def add_food():
    preparation_time = "2026-03-30T15:50:00"
    data = {
        "name": request.form.get('name'),
        # "description": request.form.get('description'),
        # "quantity": request.form.get('quantity'),
        "expiry_date": preparation_time
    }
    freshness_score = ais.calculate_freshness_score(preparation_time)
    return jsonify({"message": "Food item added successfully", "data": data, "freshness_score": freshness_score}), 201
