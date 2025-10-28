from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.material import Material
from sqlalchemy import desc, or_

materials_bp = Blueprint('materials', __name__)

@materials_bp.route('/', methods=['GET'])
@jwt_required()
def get_materials():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        category = request.args.get('category')
        location = request.args.get('location')
        search = request.args.get('search')
        
        # Build query
        query = Material.query
        
        # Filter by user role
        if user.role == 'industry':
            # Industries see their own materials
            query = query.filter_by(owner_id=user.id)
        else:
            # Artisans see available materials from others
            query = query.filter(Material.status == 'available')
        
        # Apply filters
        if category:
            query = query.filter(Material.category == category)
        
        if location:
            query = query.filter(Material.location.ilike(f'%{location}%'))
        
        if search:
            query = query.filter(
                or_(
                    Material.name.ilike(f'%{search}%'),
                    Material.description.ilike(f'%{search}%')
                )
            )
        
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

@materials_bp.route('/', methods=['POST'])
@jwt_required()
def create_material():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        if user.role != 'industry':
            return jsonify({'message': 'Only industries can create materials'}), 403
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'category', 'quantity', 'unit', 'location', 'price']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'{field} is required'}), 400
        
        # Create material
        material = Material(
            name=data['name'],
            category=data['category'],
            quantity=float(data['quantity']),
            unit=data['unit'],
            location=data['location'],
            price=float(data['price']),
            description=data.get('description', ''),
            images=data.get('images', []),
            owner_id=user_id
        )
        
        db.session.add(material)
        db.session.commit()
        
        return jsonify({
            'message': 'Material created successfully',
            'material': material.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to create material: {str(e)}'}), 500

@materials_bp.route('/<material_id>', methods=['GET'])
@jwt_required()
def get_material(material_id):
    try:
        material = Material.query.get(material_id)
        
        if not material:
            return jsonify({'message': 'Material not found'}), 404
        
        return jsonify(material.to_dict()), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to get material: {str(e)}'}), 500

@materials_bp.route('/<material_id>', methods=['PUT'])
@jwt_required()
def update_material(material_id):
    try:
        user_id = get_jwt_identity()
        material = Material.query.get(material_id)
        
        if not material:
            return jsonify({'message': 'Material not found'}), 404
        
        if material.owner_id != user_id:
            return jsonify({'message': 'Not authorized to update this material'}), 403
        
        data = request.get_json()
        
        # Update fields
        if 'name' in data:
            material.name = data['name']
        if 'category' in data:
            material.category = data['category']
        if 'quantity' in data:
            material.quantity = float(data['quantity'])
        if 'unit' in data:
            material.unit = data['unit']
        if 'location' in data:
            material.location = data['location']
        if 'price' in data:
            material.price = float(data['price'])
        if 'description' in data:
            material.description = data['description']
        if 'images' in data:
            material.images = data['images']
        if 'status' in data:
            material.status = data['status']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Material updated successfully',
            'material': material.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to update material: {str(e)}'}), 500

@materials_bp.route('/<material_id>', methods=['DELETE'])
@jwt_required()
def delete_material(material_id):
    try:
        user_id = get_jwt_identity()
        material = Material.query.get(material_id)
        
        if not material:
            return jsonify({'message': 'Material not found'}), 404
        
        if material.owner_id != user_id:
            return jsonify({'message': 'Not authorized to delete this material'}), 403
        
        db.session.delete(material)
        db.session.commit()
        
        return jsonify({'message': 'Material deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to delete material: {str(e)}'}), 500

@materials_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    try:
        # Get distinct categories
        categories = db.session.query(Material.category).distinct().all()
        category_list = [cat[0] for cat in categories if cat[0]]
        
        # Add common categories if not present
        common_categories = [
            'Metals', 'Plastics', 'Textiles', 'Paper', 'Glass', 
            'Electronics', 'Wood', 'Rubber', 'Chemicals', 'Other'
        ]
        
        for cat in common_categories:
            if cat not in category_list:
                category_list.append(cat)
        
        return jsonify({'categories': sorted(category_list)}), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to get categories: {str(e)}'}), 500