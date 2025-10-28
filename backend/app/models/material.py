from app import db
from datetime import datetime
import uuid

class Material(db.Model):
    __tablename__ = 'materials'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    images = db.Column(db.JSON)  # Store image URLs as JSON array
    status = db.Column(db.Enum('available', 'reserved', 'sold', name='material_status'), default='available')
    
    # Foreign keys
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    requests = db.relationship('Request', backref='material', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert material object to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'quantity': self.quantity,
            'unit': self.unit,
            'location': self.location,
            'price': self.price,
            'description': self.description,
            'images': self.images or [],
            'status': self.status,
            'owner_id': self.owner_id,
            'owner_name': self.owner.name if self.owner else None,
            'owner_company': self.owner.company_name if self.owner and self.owner.role == 'industry' else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Material {self.name}>'