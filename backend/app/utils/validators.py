import re

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    return len(password) >= 6

def validate_gst(gst_number):
    """Validate GST number format"""
    pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
    return re.match(pattern, gst_number) is not None

def validate_phone(phone):
    """Validate phone number format"""
    pattern = r'^[+]?[1-9]?[0-9]{7,15}$'
    return re.match(pattern, phone) is not None