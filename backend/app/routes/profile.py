from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.utils.validators import validate_email, validate_password, validate_gst

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to get profile: {str(e)}'}), 500

@profile_bp.route('/', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update basic fields
        if 'name' in data:
            user.name = data['name']
        
        if 'email' in data:
            if data['email'] != user.email:
                if not validate_email(data['email']):
                    return jsonify({'message': 'Invalid email format'}), 400
                
                # Check if email is already taken
                existing_user = User.query.filter_by(email=data['email']).first()
                if existing_user and existing_user.id != user_id:
                    return jsonify({'message': 'Email already taken'}), 400
                
                user.email = data['email']
        
        # Update role-specific fields
        if user.role == 'industry':
            if 'company_name' in data:
                user.company_name = data['company_name']
            
            if 'gst_number' in data:
                if not validate_gst(data['gst_number']):
                    return jsonify({'message': 'Invalid GST number format'}), 400
                user.gst_number = data['gst_number']
        
        elif user.role == 'artisan':
            if 'location' in data:
                user.location = data['location']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to update profile: {str(e)}'}), 500

@profile_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('current_password') or not data.get('new_password'):
            return jsonify({'message': 'Current password and new password are required'}), 400
        
        # Check current password
        if not user.check_password(data['current_password']):
            return jsonify({'message': 'Current password is incorrect'}), 400
        
        # Validate new password
        if not validate_password(data['new_password']):
            return jsonify({'message': 'New password must be at least 6 characters long'}), 400
        
        # Update password
        user.set_password(data['new_password'])
        db.session.commit()
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to change password: {str(e)}'}), 500

@profile_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_profile_stats():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        from app.models.material import Material
        from app.models.request import Request
        from app.models.transaction import Transaction
        from sqlalchemy import func
        
        stats = {}
        
        if user.role == 'industry':
            # Industry stats
            stats['total_materials'] = Material.query.filter_by(owner_id=user_id).count()
            stats['available_materials'] = Material.query.filter_by(owner_id=user_id, status='available').count()
            stats['total_requests'] = Request.query.filter_by(owner_id=user_id).count()
            stats['pending_requests'] = Request.query.filter_by(owner_id=user_id, status='pending').count()
            
            # Calculate total revenue
            total_revenue = db.session.query(func.sum(Transaction.amount)).join(Request).filter(
                Request.owner_id == user_id,
                Transaction.status == 'completed'
            ).scalar() or 0
            stats['total_revenue'] = float(total_revenue)
            
        elif user.role == 'artisan':
            # Artisan stats
            stats['total_requests'] = Request.query.filter_by(requester_id=user_id).count()
            stats['accepted_requests'] = Request.query.filter_by(requester_id=user_id, status='accepted').count()
            stats['completed_requests'] = Request.query.filter_by(requester_id=user_id, status='completed').count()
            
            # Calculate total spent
            total_spent = db.session.query(func.sum(Transaction.amount)).join(Request).filter(
                Request.requester_id == user_id,
                Transaction.status == 'completed'
            ).scalar() or 0
            stats['total_spent'] = float(total_spent)
        
        # Common stats
        stats['account_age_days'] = (db.func.current_timestamp() - user.created_at).days if user.created_at else 0
        stats['is_verified'] = user.is_verified
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to get profile stats: {str(e)}'}), 500