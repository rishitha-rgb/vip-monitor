from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.material import Material
from app.models.request import Request
from app.models.transaction import Transaction
from sqlalchemy import func, extract, desc
from datetime import datetime, timedelta

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/', methods=['GET'])
@jwt_required()
def get_analytics():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        # Get query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        location = request.args.get('location')
        
        # Parse dates
        if start_date:
            start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        else:
            start_date = datetime.utcnow() - timedelta(days=30)
        
        if end_date:
            end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        else:
            end_date = datetime.utcnow()
        
        if user.role == 'admin':
            return get_admin_analytics(start_date, end_date, location)
        else:
            return get_user_analytics(user, start_date, end_date, location)
            
    except Exception as e:
        return jsonify({'message': f'Failed to get analytics: {str(e)}'}), 500

def get_user_analytics(user, start_date, end_date, location):
    """Get analytics for individual users"""
    
    # Base queries
    if user.role == 'industry':
        materials_query = Material.query.filter_by(owner_id=user.id)
        requests_query = Request.query.filter_by(owner_id=user.id)
        transactions_query = db.session.query(Transaction).join(Request).filter(
            Request.owner_id == user.id
        )
    else:  # artisan
        materials_query = Material.query.filter(Material.status == 'available')
        requests_query = Request.query.filter_by(requester_id=user.id)
        transactions_query = db.session.query(Transaction).join(Request).filter(
            Request.requester_id == user.id
        )
    
    # Apply date filters
    materials_query = materials_query.filter(
        Material.created_at >= start_date,
        Material.created_at <= end_date
    )
    requests_query = requests_query.filter(
        Request.created_at >= start_date,
        Request.created_at <= end_date
    )
    transactions_query = transactions_query.filter(
        Transaction.created_at >= start_date,
        Transaction.created_at <= end_date
    )
    
    # Apply location filter
    if location:
        materials_query = materials_query.filter(Material.location.ilike(f'%{location}%'))
    
    # Get monthly data
    monthly_data = []
    current_date = start_date.replace(day=1)
    
    while current_date <= end_date:
        next_month = (current_date.replace(day=28) + timedelta(days=4)).replace(day=1)
        
        month_materials = materials_query.filter(
            Material.created_at >= current_date,
            Material.created_at < next_month
        ).count()
        
        month_requests = requests_query.filter(
            Request.created_at >= current_date,
            Request.created_at < next_month
        ).count()
        
        month_transactions = transactions_query.filter(
            Transaction.created_at >= current_date,
            Transaction.created_at < next_month,
            Transaction.status == 'completed'
        ).count()
        
        month_revenue = transactions_query.filter(
            Transaction.created_at >= current_date,
            Transaction.created_at < next_month,
            Transaction.status == 'completed'
        ).with_entities(func.sum(Transaction.amount)).scalar() or 0
        
        monthly_data.append({
            'month': current_date.strftime('%Y-%m'),
            'materials': month_materials,
            'requests': month_requests,
            'transactions': month_transactions,
            'revenue': float(month_revenue)
        })
        
        current_date = next_month
    
    # Get category breakdown
    category_data = db.session.query(
        Material.category,
        func.count(Material.id).label('count'),
        func.sum(Material.quantity).label('total_quantity')
    ).filter(
        Material.created_at >= start_date,
        Material.created_at <= end_date
    )
    
    if user.role == 'industry':
        category_data = category_data.filter_by(owner_id=user.id)
    
    category_data = category_data.group_by(Material.category).all()
    
    # Calculate carbon footprint saved (estimated)
    total_materials = materials_query.count()
    carbon_footprint_saved = total_materials * 2.5  # Estimated 2.5 kg CO2 per material unit
    
    return jsonify({
        'period': {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        },
        'summary': {
            'total_materials': materials_query.count(),
            'total_requests': requests_query.count(),
            'total_transactions': transactions_query.filter(Transaction.status == 'completed').count(),
            'total_revenue': float(transactions_query.filter(Transaction.status == 'completed').with_entities(func.sum(Transaction.amount)).scalar() or 0),
            'carbon_footprint_saved': carbon_footprint_saved
        },
        'monthly_data': monthly_data,
        'category_breakdown': [
            {
                'category': cat[0],
                'count': cat[1],
                'total_quantity': float(cat[2] or 0)
            }
            for cat in category_data
        ]
    }), 200

def get_admin_analytics(start_date, end_date, location):
    """Get analytics for admin users"""
    
    # Base queries
    users_query = User.query.filter(
        User.created_at >= start_date,
        User.created_at <= end_date
    )
    materials_query = Material.query.filter(
        Material.created_at >= start_date,
        Material.created_at <= end_date
    )
    requests_query = Request.query.filter(
        Request.created_at >= start_date,
        Request.created_at <= end_date
    )
    transactions_query = Transaction.query.filter(
        Transaction.created_at >= start_date,
        Transaction.created_at <= end_date
    )
    
    # Apply location filter
    if location:
        materials_query = materials_query.filter(Material.location.ilike(f'%{location}%'))
        users_query = users_query.filter(
            db.or_(
                User.location.ilike(f'%{location}%'),
                User.company_name.ilike(f'%{location}%')
            )
        )
    
    # Get platform statistics
    total_users = users_query.count()
    total_industries = users_query.filter_by(role='industry').count()
    total_artisans = users_query.filter_by(role='artisan').count()
    total_materials = materials_query.count()
    total_requests = requests_query.count()
    total_transactions = transactions_query.filter_by(status='completed').count()
    total_revenue = transactions_query.filter_by(status='completed').with_entities(func.sum(Transaction.amount)).scalar() or 0
    platform_revenue = float(total_revenue) * 0.05  # 5% commission
    
    # Get monthly growth data
    monthly_data = []
    current_date = start_date.replace(day=1)
    
    while current_date <= end_date:
        next_month = (current_date.replace(day=28) + timedelta(days=4)).replace(day=1)
        
        month_users = users_query.filter(
            User.created_at >= current_date,
            User.created_at < next_month
        ).count()
        
        month_materials = materials_query.filter(
            Material.created_at >= current_date,
            Material.created_at < next_month
        ).count()
        
        month_transactions = transactions_query.filter(
            Transaction.created_at >= current_date,
            Transaction.created_at < next_month,
            Transaction.status == 'completed'
        ).count()
        
        month_revenue = transactions_query.filter(
            Transaction.created_at >= current_date,
            Transaction.created_at < next_month,
            Transaction.status == 'completed'
        ).with_entities(func.sum(Transaction.amount)).scalar() or 0
        
        monthly_data.append({
            'month': current_date.strftime('%Y-%m'),
            'users': month_users,
            'materials': month_materials,
            'transactions': month_transactions,
            'revenue': float(month_revenue)
        })
        
        current_date = next_month
    
    # Get top locations
    location_data = db.session.query(
        Material.location,
        func.count(Material.id).label('material_count')
    ).filter(
        Material.created_at >= start_date,
        Material.created_at <= end_date
    ).group_by(Material.location).order_by(desc('material_count')).limit(10).all()
    
    # Get top categories
    category_data = db.session.query(
        Material.category,
        func.count(Material.id).label('count'),
        func.sum(Material.quantity).label('total_quantity')
    ).filter(
        Material.created_at >= start_date,
        Material.created_at <= end_date
    ).group_by(Material.category).order_by(desc('count')).all()
    
    return jsonify({
        'period': {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        },
        'summary': {
            'total_users': total_users,
            'total_industries': total_industries,
            'total_artisans': total_artisans,
            'total_materials': total_materials,
            'total_requests': total_requests,
            'total_transactions': total_transactions,
            'total_revenue': float(total_revenue),
            'platform_revenue': platform_revenue,
            'carbon_footprint_saved': total_materials * 2.5
        },
        'monthly_data': monthly_data,
        'top_locations': [
            {
                'location': loc[0],
                'material_count': loc[1]
            }
            for loc in location_data
        ],
        'category_breakdown': [
            {
                'category': cat[0],
                'count': cat[1],
                'total_quantity': float(cat[2] or 0)
            }
            for cat in category_data
        ]
    }), 200