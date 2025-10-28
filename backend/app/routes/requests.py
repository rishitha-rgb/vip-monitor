from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.material import Material
from app.models.request import Request
from app.models.transaction import Transaction
from sqlalchemy import desc, or_
from datetime import datetime

requests_bp = Blueprint('requests', __name__)

@requests_bp.route('/', methods=['GET'])
@jwt_required()
def get_requests():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status')
        request_type = request.args.get('type', 'all')  # 'sent', 'received', 'all'
        
        # Build query based on user role and request type
        if user.role == 'industry':
            if request_type == 'sent':
                query = Request.query.filter_by(requester_id=user_id)
            else:
                query = Request.query.filter_by(owner_id=user_id)
        elif user.role == 'artisan':
            if request_type == 'received':
                query = Request.query.filter_by(owner_id=user_id)
            else:
                query = Request.query.filter_by(requester_id=user_id)
        else:
            # Admin sees all requests
            query = Request.query
        
        # Apply status filter
        if status:
            query = query.filter(Request.status == status)
        
        # Order by creation date
        query = query.order_by(desc(Request.created_at))
        
        # Paginate
        requests = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'requests': [req.to_dict() for req in requests.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': requests.total,
                'pages': requests.pages,
                'has_next': requests.has_next,
                'has_prev': requests.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to get requests: {str(e)}'}), 500

@requests_bp.route('/', methods=['POST'])
@jwt_required()
def create_request():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['material_id', 'quantity']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'{field} is required'}), 400
        
        # Get material
        material = Material.query.get(data['material_id'])
        if not material:
            return jsonify({'message': 'Material not found'}), 404
        
        if material.owner_id == user_id:
            return jsonify({'message': 'Cannot request your own material'}), 400
        
        if material.status != 'available':
            return jsonify({'message': 'Material is not available'}), 400
        
        # Validate quantity
        requested_quantity = float(data['quantity'])
        if requested_quantity <= 0:
            return jsonify({'message': 'Quantity must be greater than 0'}), 400
        
        if requested_quantity > material.quantity:
            return jsonify({'message': 'Requested quantity exceeds available quantity'}), 400
        
        # Create request
        new_request = Request(
            material_id=data['material_id'],
            requester_id=user_id,
            owner_id=material.owner_id,
            quantity=requested_quantity,
            message=data.get('message', '')
        )
        
        db.session.add(new_request)
        db.session.commit()
        
        return jsonify({
            'message': 'Request created successfully',
            'request': new_request.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to create request: {str(e)}'}), 500

@requests_bp.route('/<request_id>', methods=['GET'])
@jwt_required()
def get_request(request_id):
    try:
        user_id = get_jwt_identity()
        req = Request.query.get(request_id)
        
        if not req:
            return jsonify({'message': 'Request not found'}), 404
        
        # Check if user is authorized to view this request
        if req.requester_id != user_id and req.owner_id != user_id:
            user = User.query.get(user_id)
            if not user or user.role != 'admin':
                return jsonify({'message': 'Not authorized to view this request'}), 403
        
        return jsonify(req.to_dict()), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to get request: {str(e)}'}), 500

@requests_bp.route('/<request_id>/accept', methods=['POST'])
@jwt_required()
def accept_request(request_id):
    try:
        user_id = get_jwt_identity()
        req = Request.query.get(request_id)
        
        if not req:
            return jsonify({'message': 'Request not found'}), 404
        
        if req.owner_id != user_id:
            return jsonify({'message': 'Not authorized to accept this request'}), 403
        
        if req.status != 'pending':
            return jsonify({'message': 'Request is not pending'}), 400
        
        # Update request status
        req.status = 'accepted'
        req.updated_at = datetime.utcnow()
        
        # Update material quantity
        material = req.material
        material.quantity -= req.quantity
        
        # If material quantity becomes 0, mark as sold
        if material.quantity <= 0:
            material.status = 'sold'
        
        # Create transaction
        transaction = Transaction(
            request_id=req.id,
            amount=req.quantity * material.price,
            status='pending',
            payment_method='escrow'
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({
            'message': 'Request accepted successfully',
            'request': req.to_dict(),
            'transaction': transaction.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to accept request: {str(e)}'}), 500

@requests_bp.route('/<request_id>/reject', methods=['POST'])
@jwt_required()
def reject_request(request_id):
    try:
        user_id = get_jwt_identity()
        req = Request.query.get(request_id)
        
        if not req:
            return jsonify({'message': 'Request not found'}), 404
        
        if req.owner_id != user_id:
            return jsonify({'message': 'Not authorized to reject this request'}), 403
        
        if req.status != 'pending':
            return jsonify({'message': 'Request is not pending'}), 400
        
        # Update request status
        req.status = 'rejected'
        req.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Request rejected successfully',
            'request': req.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to reject request: {str(e)}'}), 500

@requests_bp.route('/<request_id>/complete', methods=['POST'])
@jwt_required()
def complete_request(request_id):
    try:
        user_id = get_jwt_identity()
        req = Request.query.get(request_id)
        
        if not req:
            return jsonify({'message': 'Request not found'}), 404
        
        # Both requester and owner can mark as complete
        if req.requester_id != user_id and req.owner_id != user_id:
            return jsonify({'message': 'Not authorized to complete this request'}), 403
        
        if req.status != 'accepted':
            return jsonify({'message': 'Request must be accepted before completion'}), 400
        
        # Update request status
        req.status = 'completed'
        req.updated_at = datetime.utcnow()
        
        # Update transaction status
        transaction = Transaction.query.filter_by(request_id=req.id).first()
        if transaction:
            transaction.status = 'completed'
            transaction.completed_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Request completed successfully',
            'request': req.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to complete request: {str(e)}'}), 500