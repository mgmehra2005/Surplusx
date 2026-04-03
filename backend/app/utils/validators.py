"""Input validation and sanitization utilities for security."""

import re
from datetime import datetime, timedelta
from markupsafe import escape


def normalize_email(email):
    """Convert email to lowercase for consistent comparison.
    
    Args:
        email (str): Email address to normalize
        
    Returns:
        str: Lowercase email, or None if input is None
    """
    if not email:
        return None
    return email.strip().lower()


def validate_email_format(email):
    """Validate email format using regex.
    
    Args:
        email (str): Email to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))


def sanitize_input(text, max_length=255, allow_special=False):
    """Sanitize user input to prevent XSS and injection attacks.
    
    Args:
        text (str): Input text to sanitize
        max_length (int): Maximum length allowed (default 255)
        allow_special (bool): Whether to allow special characters (default False)
        
    Returns:
        str: Sanitized text
        
    Raises:
        ValueError: If input is invalid
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    
    # Strip whitespace
    text = text.strip()
    
    # Limit length
    text = text[:max_length]
    
    # Remove potentially dangerous characters if not allowed
    if not allow_special:
        # Keep only alphanumeric, spaces, and common punctuation
        text = re.sub(r'[<>"\'{};\\]', '', text)
    
    # HTML escape to prevent XSS
    text = escape(text)
    
    return str(text)


def validate_name(name):
    """Validate user name format.
    
    Args:
        name (str): Name to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(name, str):
        return False
    
    name = name.strip()
    
    # Allow letters, numbers, spaces, hyphens, and apostrophes
    pattern = r"^[a-zA-Z0-9\s\-']+$"
    
    return bool(re.match(pattern, name)) and len(name) >= 2 and len(name) <= 100


def validate_password_strength(password):
    """Validate password meets minimum requirements.
    
    Args:
        password (str): Password to validate
        
    Returns:
        tuple: (is_valid, message) where is_valid is bool and message describes issues
    """
    if not isinstance(password, str):
        return False, "Password must be a string"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if len(password) > 128:
        return False, "Password must be less than 128 characters"
    
    # Check for uppercase
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    # Check for lowercase
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    # Check for digit
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    # Check for special character
    if not re.search(r'[!@#$%^&*()_+=\-\[\]{};:\'",.<>?/\\|`~]', password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is valid"


def validate_phone(phone):
    """Validate phone number format.
    
    Args:
        phone (str): Phone number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not phone:
        return True  # Phone is optional
    
    if not isinstance(phone, str):
        return False
    
    # Allow digits, spaces, hyphens, plus sign
    pattern = r'^[\d\s\-+()]+$'
    
    return bool(re.match(pattern, phone)) and len(phone) >= 10


def validate_date_range(date_str, allow_past=False):
    """Validate date string and ensure it's within reasonable range.
    
    Args:
        date_str (str): ISO format date string
        allow_past (bool): Whether to allow dates in the past
        
    Returns:
        tuple: (is_valid, datetime_obj, message)
    """
    try:
        dt = datetime.fromisoformat(date_str)
        
        # Check not too far in future (max 10 years)
        max_future = datetime.utcnow() + timedelta(days=365*10)
        if dt > max_future:
            return False, None, "Date is too far in the future"
        
        # Check not too far in past (unless allowed)
        if not allow_past and dt < datetime.utcnow():
            return False, None, "Date cannot be in the past"
        
        return True, dt, "Date is valid"
        
    except (ValueError, TypeError) as e:
        return False, None, f"Invalid date format. Use ISO 8601 (YYYY-MM-DDTHH:MM:SS): {str(e)}"


def validate_quantity(quantity, min_value=0.01, max_value=1000000):
    """Validate quantity value.
    
    Args:
        quantity: Quantity to validate (will be converted to float)
        min_value (float): Minimum allowed value
        max_value (float): Maximum allowed value
        
    Returns:
        tuple: (is_valid, float_value, message)
    """
    try:
        qty = float(quantity)
        
        if qty < min_value:
            return False, None, f"Quantity must be at least {min_value}"
        
        if qty > max_value:
            return False, None, f"Quantity must be at most {max_value}"
        
        return True, qty, "Quantity is valid"
        
    except (ValueError, TypeError):
        return False, None, "Quantity must be a number"


def validate_enum(value, allowed_values, field_name="field"):
    """Validate that a value is in allowed list.
    
    Args:
        value: Value to check
        allowed_values (list): List of valid values
        field_name (str): Name of field for error message
        
    Returns:
        tuple: (is_valid, message)
    """
    if value not in allowed_values:
        return False, f"Invalid {field_name}. Must be one of: {', '.join(allowed_values)}"
    
    return True, f"{field_name} is valid"


def safe_json_parse(json_string, default=None):
    """Safely parse JSON string.
    
    Args:
        json_string (str): JSON string to parse
        default: Default value if parsing fails
        
    Returns:
        dict or default: Parsed JSON or default value
    """
    import json
    
    try:
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError):
        return default


def validate_coordinates(latitude, longitude):
    """Validate geographic coordinates.
    
    Args:
        latitude: Latitude value
        longitude: Longitude value
        
    Returns:
        tuple: (is_valid, message)
    """
    try:
        lat = float(latitude)
        lon = float(longitude)
        
        if not (-90 <= lat <= 90):
            return False, "Latitude must be between -90 and 90"
        
        if not (-180 <= lon <= 180):
            return False, "Longitude must be between -180 and 180"
        
        return True, "Coordinates are valid"
        
    except (ValueError, TypeError):
        return False, "Coordinates must be numbers"
