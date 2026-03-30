import numpy as np
from datetime import datetime, timedelta

def calculate_freshness_score(preparation_time, current_time=None):
    """
    Calculate freshness score based on time since preparation
    
    Args:
        preparation_time (str/datetime): When food was prepared
        current_time (str/datetime): Current time (defaults to now)
        
    Returns:
        float: Freshness score (0-1, where 1 is freshest)
    """
    if current_time is None:
        current_time = datetime.now()
    
    # Convert to datetime if strings
    if isinstance(preparation_time, str):
        preparation_time = datetime.fromisoformat(preparation_time)
    if isinstance(current_time, str):
        current_time = datetime.fromisoformat(current_time)
    
    # Calculate time difference in hours
    time_diff = current_time - preparation_time
    hours_since_prep = time_diff.total_seconds() / 3600
    
    # Freshness decays exponentially over 24 hours
    # Score = 1 when fresh (0 hours), approaches 0 at 24 hours
    freshness_score = max(0, 1 - (hours_since_prep / 24))
    
    return float(freshness_score)

def calculate_spoilage_risk(food_type, temperature, time_since_prep_hours):
    """
    Calculate spoilage risk based on food type, temperature, and time
    
    Args:
        food_type (str): Type of food (prepared, raw, packaged, baked)
        temperature (float): Storage temperature in Celsius
        time_since_prep_hours (float): Hours since preparation
        
    Returns:
        float: Spoilage risk (0-1, where 1 is high risk)
    """
    # Base spoilage rates by food type (per hour)
    spoilage_rates = {
        'prepared': 0.08,   # Cooked food spoils faster
        'raw': 0.06,        # Raw ingredients
        'packaged': 0.02,   # Packaged goods last longer
        'baked': 0.05       # Baked goods
    }
    
    base_rate = spoilage_rates.get(food_type, 0.05)
    
    # Temperature adjustment
    # Ideal temp range: 0-4°C (refrigerated)
    if temperature < 0:
        temp_factor = 0.5  # Freezing slows spoilage
    elif temperature <= 4:
        temp_factor = 1.0  # Ideal refrigeration
    elif temperature <= 20:
        temp_factor = 1.5  # Room temp accelerates spoilage
    else:
        temp_factor = 2.0  # Warm temps significantly increase spoilage
    
    # Calculate spoilage risk
    effective_rate = base_rate * temp_factor
    spoilage_risk = min(1.0, time_since_prep_hours * effective_rate)
    
    return float(spoilage_risk)

def calculate_edibility_score(freshness_score, spoilage_risk, food_type):
    """
    Calculate overall edibility score
    
    Args:
        freshness_score (float): Freshness score (0-1)
        spoilage_risk (float): Spoilage risk (0-1)
        food_type (str): Type of food
        
    Returns:
        dict: Edibility assessment with score and recommendation
    """
    # Weighted combination
    edibility_score = (freshness_score * 0.6) - (spoilage_risk * 0.4)
    edibility_score = max(0, min(1, edibility_score))  # Clamp to 0-1
    
    # Determine recommendation
    if edibility_score >= 0.8:
        recommendation = "HIGH_QUALITY"
        description = "Excellent condition, safe to consume"
    elif edibility_score >= 0.6:
        recommendation = "GOOD"
        description = "Good condition, safe to consume"
    elif edibility_score >= 0.4:
        recommendation = "FAIR"
        description = "Acceptable condition, consume soon"
    elif edibility_score >= 0.2:
        recommendation = "POOR"
        description = "Poor condition, use for cooking only"
    else:
        recommendation = "UNSAFE"
        description = "Not recommended for consumption"
    
    return {
        "edibility_score": float(edibility_score),
        "recommendation": recommendation,
        "description": description,
        "freshness_score": float(freshness_score),
        "spoilage_risk": float(spoilage_risk),
        "food_type": food_type
    }