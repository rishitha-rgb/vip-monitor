from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.material import Material
from app.models.request import Request
from app.models.transaction import Transaction
from sqlalchemy import func, desc

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/', methods=['GET'])
@jwt_required()
def get_dashboard_data():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        if user.role == 'industry':
            return get_industry_dashboard(user)
        elif user.role == 'artisan':
            return get_artisan_dashboard(user)
        elif user.role == 'admin':
            return get_admin_dashboard(user)
        else:
            return jsonify({'message': 'Invalid user role'}), 400
            
    except Exception as e:
        return jsonify({'message': f'Failed to get dashboard data: {str(e)}'}), 500

def get_industry_dashboard(user):
    """Get dashboard data for industry users"""
    # Get materials count
    materials_count = Material.query.filter_by(owner_id=user.id).count()
    available_materials = Material.query.filter_by(owner_id=user.id, status='available').count()
    
    # Get requests count
    received_requests = Request.query.filter_by(owner_id=user.id).count()
    pending_requests = Request.query.filter_by(owner_id=user.id, status='pending').count()
    
    # Get transactions
    transactions = db.session.query(Transaction).join(Request).filter(
        Request.owner_id == user.id
    ).count()
    
    # Calculate total revenue
    total_revenue = db.session.query(func.sum(Transaction.amount)).join(Request).filter(
        Request.owner_id == user.id,
        Transaction.status == 'completed'
    ).scalar() or 0
    
    # Get recent materials
    recent_materials = Material.query.filter_by(owner_id=user.id).order_by(
        desc(Material.created_at)
    ).limit(5).all()
    
    # Get recent requests
    recent_requests = Request.query.filter_by(owner_id=user.id).order_by(
        desc(Request.created_at)
    ).limit(5).all()
    
    return jsonify({
        'user_type': 'industry',
        'stats': {
            'total_materials': materials_count,
            'available_materials': available_materials,
            'total_requests': received_requests,
            'pending_requests': pending_requests,
            'total_transactions': transactions,
            'total_revenue': total_revenue
        },
        'recent_materials': [material.to_dict() for material in recent_materials],
        'recent_requests': [request.to_dict() for request in recent_requests]
    }), 200

def get_artisan_dashboard(user):
    """Get dashboard data for artisan users"""
    # Get requests count
    sent_requests = Request.query.filter_by(requester_id=user.id).count()
    accepted_requests = Request.query.filter_by(requester_id=user.id, status='accepted').count()
    
    # Get available materials in user's location
    available_materials = Material.query.filter(
        Material.location.ilike(f'%{user.location}%'),
        Material.status == 'available'
    ).count() if user.location else 0
    
    # Calculate total spent
    total_spent = db.session.query(func.sum(Transaction.amount)).join(Request).filter(
        Request.requester_id == user.id,
        Transaction.status == 'completed'
    ).scalar() or 0
    
    # Get recent available materials
    recent_materials = Material.query.filter(
        Material.status == 'available'
    ).order_by(desc(Material.created_at)).limit(10).all()
    
    # Get user's recent requests
    recent_requests = Request.query.filter_by(requester_id=user.id).order_by(
        desc(Request.created_at)
    ).limit(5).all()
    
    return jsonify({
        'user_type': 'artisan',
        'stats': {
            'total_requests': sent_requests,
            'accepted_requests': accepted_requests,
            'available_materials': available_materials,
            'total_spent': total_spent
        },
        'available_materials': [material.to_dict() for material in recent_materials],
        'recent_requests': [request.to_dict() for request in recent_requests]
    }), 200

def get_admin_dashboard(user):
    """Get dashboard data for admin users"""
    # Get overall stats
    total_users = User.query.count()
    total_industries = User.query.filter_by(role='industry').count()
    total_artisans = User.query.filter_by(role='artisan').count()
    total_materials = Material.query.count()
    total_requests = Request.query.count()
    total_transactions = Transaction.query.count()
    
    # Calculate total platform revenue (assuming 5% commission)
    total_revenue = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.status == 'completed'
    ).scalar() or 0
    platform_revenue = total_revenue * 0.05
    
    # Get recent activities
    recent_users = User.query.order_by(desc(User.created_at)).limit(5).all()
    recent_materials = Material.query.order_by(desc(Material.created_at)).limit(5).all()
    recent_requests = Request.query.order_by(desc(Request.created_at)).limit(5).all()
    
    return jsonify({
        'user_type': 'admin',
        'stats': {
            'total_users': total_users,
            'total_industries': total_industries,
            'total_artisans': total_artisans,
            'total_materials': total_materials,
            'total_requests': total_requests,
            'total_transactions': total_transactions,
            'platform_revenue': platform_revenue
        },
        'recent_users': [user.to_dict() for user in recent_users],
        'recent_materials': [material.to_dict() for material in recent_materials],
        'recent_requests': [request.to_dict() for request in recent_requests]
    }), 200