from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.material import Material
from app.models.request import Request
from app.models.transaction import Transaction
from sqlalchemy import desc, func

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator to require admin role"""
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_users():
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        role = request.args.get('role')
        search = request.args.get('search')
        
        # Build query
        query = User.query
        
        if role:
            query = query.filter_by(role=role)
        
        if search:
            query = query.filter(
                db.or_(
                    User.name.ilike(f'%{search}%'),
                    User.email.ilike(f'%{search}%'),
                    User.company_name.ilike(f'%{search}%')
                )
            )
        
        # Order by creation date
        query = query.order_by(desc(User.created_at))
        
        # Paginate
        users = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'users': [user.to_dict() for user in users.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': users.total,
                'pages': users.pages,
                'has_next': users.has_next,
                'has_prev': users.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to get users: {str(e)}'}), 500

@admin_bp.route('/users/<user_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        # Get user statistics
        user_data = user.to_dict()
        
        # Add statistics
        if user.role == 'industry':
            user_data['stats'] = {
                'total_materials': Material.query.filter_by(owner_id=user_id).count(),
                'total_requests': Request.query.filter_by(owner_id=user_id).count(),
                'total_revenue': db.session.query(func.sum(Transaction.amount)).join(Request).filter(
                    Request.owner_id == user_id,
                    Transaction.status == 'completed'
                ).scalar() or 0
            }
        elif user.role == 'artisan':
            user_data['stats'] = {
                'total_requests': Request.query.filter_by(requester_id=user_id).count(),
                'accepted_requests': Request.query.filter_by(requester_id=user_id, status='accepted').count(),
                'total_spent': db.session.query(func.sum(Transaction.amount)).join(Request).filter(
                    Request.requester_id == user_id,
                    Transaction.status == 'completed'
                ).scalar() or 0
            }
        
        return jsonify(user_data), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to get user: {str(e)}'}), 500

@admin_bp.route('/users/<user_id>/toggle-status', methods=['POST'])
@jwt_required()
@admin_required
def toggle_user_status(user_id):
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        if user.role == 'admin':
            return jsonify({'message': 'Cannot modify admin users'}), 400
        
        # Toggle active status
        user.is_active = not user.is_active
        db.session.commit()
        
        status = 'activated' if user.is_active else 'deactivated'
        
        return jsonify({
            'message': f'User {status} successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to toggle user status: {str(e)}'}), 500

@admin_bp.route('/users/<user_id>/verify', methods=['POST'])
@jwt_required()
@admin_required
def verify_user(user_id):
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        user.is_verified = True
        db.session.commit()
        
        return jsonify({
            'message': 'User verified successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to verify user: {str(e)}'}), 500

@admin_bp.route('/materials', methods=['GET'])
@jwt_required()
@admin_required
def get_all_materials():
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        category = request.args.get('category')
        status = request.args.get('status')
        
        # Build query
        query = Material.query
        
        if category:
            query = query.filter_by(category=category)
        
        if status:
            query = query.filter_by(status=status)
        
        # Order by creation date
        query = query.order_by(desc(Material.created_at))
        
        # Paginate
        materials = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'materials': [material.to_dict() for material in materials.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': materials.total,
                'pages': materials.pages,
                'has_next': materials.has_next,
                'has_prev': materials.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to get materials: {str(e)}'}), 500

@admin_bp.route('/transactions', methods=['GET'])
@jwt_required()
@admin_required
def get_all_transactions():
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        
        # Build query
        query = Transaction.query
        
        if status:
            query = query.filter_by(status=status)
        
        # Order by creation date
        query = query.order_by(desc(Transaction.created_at))
        
        # Paginate
        transactions = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'transactions': [transaction.to_dict() for transaction in transactions.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': transactions.total,
                'pages': transactions.pages,
                'has_next': transactions.has_next,
                'has_prev': transactions.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to get transactions: {str(e)}'}), 500

@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@admin_required
def get_admin_dashboard():
    try:
        # Get overall statistics
        total_users = User.query.count()
        total_industries = User.query.filter_by(role='industry').count()
        total_artisans = User.query.filter_by(role='artisan').count()
        active_users = User.query.filter_by(is_active=True).count()
        verified_users = User.query.filter_by(is_verified=True).count()
        
        total_materials = Material.query.count()
        available_materials = Material.query.filter_by(status='available').count()
        
        total_requests = Request.query.count()
        pending_requests = Request.query.filter_by(status='pending').count()
        completed_requests = Request.query.filter_by(status='completed').count()
        
        total_transactions = Transaction.query.count()
        completed_transactions = Transaction.query.filter_by(status='completed').count()
        
        # Calculate revenue
        total_revenue = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.status == 'completed'
        ).scalar() or 0
        platform_revenue = float(total_revenue) * 0.05  # 5% commission
        
        # Get recent activities
        recent_users = User.query.order_by(desc(User.created_at)).limit(5).all()
        recent_materials = Material.query.order_by(desc(Material.created_at)).limit(5).all()
        recent_transactions = Transaction.query.order_by(desc(Transaction.created_at)).limit(5).all()
        
        return jsonify({
            'stats': {
                'users': {
                    'total': total_users,
                    'industries': total_industries,
                    'artisans': total_artisans,
                    'active': active_users,
                    'verified': verified_users
                },
                'materials': {
                    'total': total_materials,
                    'available': available_materials
                },
                'requests': {
                    'total': total_requests,
                    'pending': pending_requests,
                    'completed': completed_requests
                },
                'transactions': {
                    'total': total_transactions,
                    'completed': completed_transactions,
                    'total_revenue': float(total_revenue),
                    'platform_revenue': platform_revenue
                }
            },
            'recent_activities': {
                'users': [user.to_dict() for user in recent_users],
                'materials': [material.to_dict() for material in recent_materials],
                'transactions': [transaction.to_dict() for transaction in recent_transactions]
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to get admin dashboard: {str(e)}'}), 500