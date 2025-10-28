from app import db, bcrypt
from datetime import datetime
from flask_jwt_extended import create_access_token
import uuid

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum('industry', 'artisan', 'admin', name='user_roles'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    
    # Industry-specific fields
    company_name = db.Column(db.String(200))
    gst_number = db.Column(db.String(15))
    
    # Artisan-specific fields
    location = db.Column(db.String(100))
    
    # Common fields
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    materials = db.relationship('Material', backref='owner', lazy=True, cascade='all, delete-orphan')
    sent_requests = db.relationship('Request', foreign_keys='Request.requester_id', backref='requester', lazy=True)
    received_requests = db.relationship('Request', foreign_keys='Request.owner_id', backref='owner', lazy=True)
    
    def __init__(self, email, password, role, name, **kwargs):
        self.email = email
        self.set_password(password)
        self.role = role
        self.name = name
        
        # Set role-specific fields
        if role == 'industry':
            self.company_name = kwargs.get('company_name')
            self.gst_number = kwargs.get('gst_number')
        elif role == 'artisan':
            self.location = kwargs.get('location')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def generate_token(self):
        """Generate JWT access token"""
        return create_access_token(identity=self.id)
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'name': self.name,
            'company_name': self.company_name,
            'gst_number': self.gst_number,
            'location': self.location,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<User {self.email}>'