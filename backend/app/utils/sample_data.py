from app import db
from app.models.user import User
from app.models.material import Material
from app.models.request import Request
from app.models.transaction import Transaction
from datetime import datetime, timedelta
import random

def create_sample_data():
    """Create sample data for the application"""
    
    # Check if data already exists
    if User.query.count() > 0:
        return
    
    print("Creating sample data...")
    
    # Create admin user
    admin = User(
        email='admin@ecocycleconnect.com',
        password='admin123',
        role='admin',
        name='System Administrator'
    )
    admin.is_verified = True
    db.session.add(admin)
    
    # Create sample industry users
    industries = [
        {
            'email': 'contact@tatasteels.com',
            'password': 'industry123',
            'name': 'Rajesh Kumar',
            'company_name': 'Tata Steel Limited',
            'gst_number': '27AAACT2727Q1ZZ'
        },
        {
            'email': 'waste@reliancetextiles.com',
            'password': 'industry123',
            'name': 'Priya Sharma',
            'company_name': 'Reliance Textiles Pvt Ltd',
            'gst_number': '24AABCR1234M1Z5'
        },
        {
            'email': 'materials@mahindragroup.com',
            'password': 'industry123',
            'name': 'Amit Patel',
            'company_name': 'Mahindra Manufacturing',
            'gst_number': '29AADCM1234N1ZX'
        },
        {
            'email': 'sustainability@infosys.com',
            'password': 'industry123',
            'name': 'Sunita Reddy',
            'company_name': 'Infosys Limited',
            'gst_number': '29AABCI1234F1Z5'
        }
    ]
    
    industry_users = []
    for industry_data in industries:
        user = User(
            email=industry_data['email'],
            password=industry_data['password'],
            role='industry',
            name=industry_data['name'],
            company_name=industry_data['company_name'],
            gst_number=industry_data['gst_number']
        )
        user.is_verified = True
        industry_users.append(user)
        db.session.add(user)
    
    # Create sample artisan users
    artisans = [
        {
            'email': 'ravi.craftsman@gmail.com',
            'password': 'artisan123',
            'name': 'Ravi Vishwakarma',
            'location': 'Mumbai, Maharashtra'
        },
        {
            'email': 'meera.weaver@gmail.com',
            'password': 'artisan123',
            'name': 'Meera Devi',
            'location': 'Jaipur, Rajasthan'
        },
        {
            'email': 'kumar.metalwork@gmail.com',
            'password': 'artisan123',
            'name': 'Kumar Singh',
            'location': 'Delhi, NCR'
        },
        {
            'email': 'lakshmi.pottery@gmail.com',
            'password': 'artisan123',
            'name': 'Lakshmi Nair',
            'location': 'Kochi, Kerala'
        },
        {
            'email': 'arjun.woodcraft@gmail.com',
            'password': 'artisan123',
            'name': 'Arjun Yadav',
            'location': 'Pune, Maharashtra'
        }
    ]
    
    artisan_users = []
    for artisan_data in artisans:
        user = User(
            email=artisan_data['email'],
            password=artisan_data['password'],
            role='artisan',
            name=artisan_data['name'],
            location=artisan_data['location']
        )
        user.is_verified = True
        artisan_users.append(user)
        db.session.add(user)
    
    db.session.commit()
    
    # Create sample materials
    materials_data = [
        {
            'name': 'Steel Scrap - Grade A',
            'category': 'Metals',
            'quantity': 500.0,
            'unit': 'kg',
            'location': 'Mumbai, Maharashtra',
            'price': 45.0,
            'description': 'High-quality steel scrap suitable for recycling and crafting',
            'owner': industry_users[0]
        },
        {
            'name': 'Cotton Fabric Waste',
            'category': 'Textiles',
            'quantity': 200.0,
            'unit': 'meters',
            'location': 'Ahmedabad, Gujarat',
            'price': 25.0,
            'description': 'Pure cotton fabric waste in various colors, perfect for handicrafts',
            'owner': industry_users[1]
        },
        {
            'name': 'Aluminum Sheets',
            'category': 'Metals',
            'quantity': 150.0,
            'unit': 'pieces',
            'location': 'Pune, Maharashtra',
            'price': 120.0,
            'description': 'Thin aluminum sheets from automotive manufacturing',
            'owner': industry_users[2]
        },
        {
            'name': 'Plastic Bottles (PET)',
            'category': 'Plastics',
            'quantity': 1000.0,
            'unit': 'pieces',
            'location': 'Bangalore, Karnataka',
            'price': 2.5,
            'description': 'Clean PET bottles suitable for upcycling projects',
            'owner': industry_users[3]
        },
        {
            'name': 'Copper Wire Scraps',
            'category': 'Metals',
            'quantity': 75.0,
            'unit': 'kg',
            'location': 'Chennai, Tamil Nadu',
            'price': 650.0,
            'description': 'Pure copper wire scraps from electrical installations',
            'owner': industry_users[0]
        },
        {
            'name': 'Cardboard Sheets',
            'category': 'Paper',
            'quantity': 300.0,
            'unit': 'sheets',
            'location': 'Delhi, NCR',
            'price': 15.0,
            'description': 'Large cardboard sheets from packaging industry',
            'owner': industry_users[1]
        },
        {
            'name': 'Glass Bottles',
            'category': 'Glass',
            'quantity': 500.0,
            'unit': 'pieces',
            'location': 'Jaipur, Rajasthan',
            'price': 8.0,
            'description': 'Various colored glass bottles for decorative crafts',
            'owner': industry_users[2]
        },
        {
            'name': 'Rubber Sheets',
            'category': 'Rubber',
            'quantity': 100.0,
            'unit': 'sheets',
            'location': 'Kochi, Kerala',
            'price': 85.0,
            'description': 'Industrial rubber sheets suitable for various applications',
            'owner': industry_users[3]
        }
    ]
    
    materials = []
    for material_data in materials_data:
        material = Material(
            name=material_data['name'],
            category=material_data['category'],
            quantity=material_data['quantity'],
            unit=material_data['unit'],
            location=material_data['location'],
            price=material_data['price'],
            description=material_data['description'],
            owner_id=material_data['owner'].id,
            images=['https://via.placeholder.com/400x300?text=' + material_data['name'].replace(' ', '+')]
        )
        materials.append(material)
        db.session.add(material)
    
    db.session.commit()
    
    # Create sample requests
    requests_data = [
        {
            'material': materials[0],  # Steel Scrap
            'requester': artisan_users[2],  # Kumar Singh
            'quantity': 50.0,
            'message': 'I need steel scrap for making decorative metal art pieces. Can you provide 50kg?',
            'status': 'pending'
        },
        {
            'material': materials[1],  # Cotton Fabric
            'requester': artisan_users[1],  # Meera Devi
            'quantity': 25.0,
            'message': 'Looking for cotton fabric waste for traditional Rajasthani handicrafts.',
            'status': 'accepted'
        },
        {
            'material': materials[3],  # Plastic Bottles
            'requester': artisan_users[0],  # Ravi Vishwakarma
            'quantity': 100.0,
            'message': 'Need PET bottles for creating eco-friendly planters and decorative items.',
            'status': 'completed'
        },
        {
            'material': materials[6],  # Glass Bottles
            'requester': artisan_users[1],  # Meera Devi
            'quantity': 50.0,
            'message': 'Colored glass bottles needed for traditional lamp making.',
            'status': 'accepted'
        },
        {
            'material': materials[4],  # Copper Wire
            'requester': artisan_users[2],  # Kumar Singh
            'quantity': 10.0,
            'message': 'Copper wire needed for jewelry making and electrical crafts.',
            'status': 'pending'
        }
    ]
    
    sample_requests = []
    for req_data in requests_data:
        request_obj = Request(
            material_id=req_data['material'].id,
            requester_id=req_data['requester'].id,
            owner_id=req_data['material'].owner_id,
            quantity=req_data['quantity'],
            message=req_data['message'],
            status=req_data['status']
        )
        
        # Set created_at to random date in the past 30 days
        days_ago = random.randint(1, 30)
        request_obj.created_at = datetime.utcnow() - timedelta(days=days_ago)
        
        sample_requests.append(request_obj)
        db.session.add(request_obj)
    
    db.session.commit()
    
    # Create sample transactions for accepted/completed requests
    for request_obj in sample_requests:
        if request_obj.status in ['accepted', 'completed']:
            transaction = Transaction(
                request_id=request_obj.id,
                amount=request_obj.quantity * request_obj.material.price,
                status='completed' if request_obj.status == 'completed' else 'pending',
                payment_method='escrow',
                transaction_reference=f'TXN{random.randint(100000, 999999)}'
            )
            
            if request_obj.status == 'completed':
                transaction.completed_at = datetime.utcnow() - timedelta(days=random.randint(1, 15))
            
            db.session.add(transaction)
    
    db.session.commit()
    
    print("Sample data created successfully!")
    print(f"Created {len(industry_users)} industry users")
    print(f"Created {len(artisan_users)} artisan users")
    print(f"Created {len(materials)} materials")
    print(f"Created {len(sample_requests)} requests")
    print("Admin user: admin@ecocycleconnect.com / admin123")
    print("Industry user: contact@tatasteels.com / industry123")
    print("Artisan user: ravi.craftsman@gmail.com / artisan123")