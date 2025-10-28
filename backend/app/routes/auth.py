from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.utils.validators import validate_email, validate_password, validate_gst

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'role', 'name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'{field} is required'}), 400
        
        # Validate email format
        if not validate_email(data['email']):
            return jsonify({'message': 'Invalid email format'}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already registered'}), 400
        
        # Validate password
        if not validate_password(data['password']):
            return jsonify({'message': 'Password must be at least 6 characters long'}), 400
        
        # Role-specific validation
        if data['role'] == 'industry':
            if not data.get('company_name'):
                return jsonify({'message': 'Company name is required for industries'}), 400
            if not data.get('gst_number'):
                return jsonify({'message': 'GST number is required for industries'}), 400
            if not validate_gst(data['gst_number']):
                return jsonify({'message': 'Invalid GST number format'}), 400
        elif data['role'] == 'artisan':
            if not data.get('location'):
                return jsonify({'message': 'Location is required for artisans'}), 400
        
        # Create new user
        user = User(
            email=data['email'],
            password=data['password'],
            role=data['role'],
            name=data['name'],
            company_name=data.get('company_name'),
            gst_number=data.get('gst_number'),
            location=data.get('location')
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Generate token
        token = user.generate_token()
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'token': token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Registration failed: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Email and password are required'}), 400
        
        # Find user
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'message': 'Invalid email or password'}), 401
        
        if not user.is_active:
            return jsonify({'message': 'Account is deactivated'}), 401
        
        # Generate token
        token = user.generate_token()
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'token': token
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Login failed: {str(e)}'}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to get user data: {str(e)}'}), 500

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    try:
        data = request.get_json()
        
        if not data.get('email'):
            return jsonify({'message': 'Email is required'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if user:
            # In a real application, you would send an email with a reset link
            # For demo purposes, we'll just return a success message
            pass
        
        # Always return success to prevent email enumeration
        return jsonify({'message': 'If the email exists, a reset link has been sent'}), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to process request: {str(e)}'}), 500

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        
        # In a real application, you would validate the reset token
        # For demo purposes, we'll just return a success message
        
        return jsonify({'message': 'Password reset successful'}), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to reset password: {str(e)}'}), 500