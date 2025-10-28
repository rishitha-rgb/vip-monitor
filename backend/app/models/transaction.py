from app import db
from datetime import datetime
import uuid

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum('pending', 'completed', 'failed', 'refunded', name='transaction_status'), default='pending')
    payment_method = db.Column(db.String(50), default='escrow')
    transaction_reference = db.Column(db.String(100))
    
    # Foreign keys
    request_id = db.Column(db.String(36), db.ForeignKey('requests.id'), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def to_dict(self):
        """Convert transaction object to dictionary"""
        return {
            'id': self.id,
            'amount': self.amount,
            'status': self.status,
            'payment_method': self.payment_method,
            'transaction_reference': self.transaction_reference,
            'request_id': self.request_id,
            'material_name': self.request.material.name if self.request and self.request.material else None,
            'requester_name': self.request.requester.name if self.request and self.request.requester else None,
            'owner_name': self.request.owner.name if self.request and self.request.owner else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    def __repr__(self):
        return f'<Transaction {self.id}>'