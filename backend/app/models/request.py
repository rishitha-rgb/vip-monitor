from app import db
from datetime import datetime
import uuid

class Request(db.Model):
    __tablename__ = 'requests'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    quantity = db.Column(db.Float, nullable=False)
    message = db.Column(db.Text)
    status = db.Column(db.Enum('pending', 'accepted', 'rejected', 'completed', name='request_status'), default='pending')
    
    # Foreign keys
    material_id = db.Column(db.String(36), db.ForeignKey('materials.id'), nullable=False)
    requester_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    transactions = db.relationship('Transaction', backref='request', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert request object to dictionary"""
        return {
            'id': self.id,
            'quantity': self.quantity,
            'message': self.message,
            'status': self.status,
            'material_id': self.material_id,
            'material_name': self.material.name if self.material else None,
            'material_category': self.material.category if self.material else None,
            'material_price': self.material.price if self.material else None,
            'requester_id': self.requester_id,
            'requester_name': self.requester.name if self.requester else None,
            'requester_location': self.requester.location if self.requester and self.requester.role == 'artisan' else None,
            'owner_id': self.owner_id,
            'owner_name': self.owner.name if self.owner else None,
            'owner_company': self.owner.company_name if self.owner and self.owner.role == 'industry' else None,
            'total_amount': self.quantity * self.material.price if self.material else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Request {self.id}>'