from flask import Blueprint, jsonify, request
from db.db import db
from services.sync_service import SyncService
from models.models import Purchase

sync_service = SyncService(db=db)
purchase_bp = Blueprint("purchases", __name__)

@purchase_bp.route('/purchases')
def purchases():
    page = request.args.get('page', 1, type=int)
    purchases = Purchase.query.order_by(Purchase.date.desc()).all()
    return jsonify(
            {
                "purchases":[p.to_dict() for p in purchases]
            })

@purchase_bp.route('/purchases_sync')
def sync_purchases():
    try:
        new_purchases,skipped_purchases = sync_service.sync()
        message = f'Sync completed: {new_purchases} new purchases added, {skipped_purchases} duplicates skipped'
        return jsonify({'success': True, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@purchase_bp.route('/api/purchases')
def api_purchases():
    purchases = Purchase.query.order_by(Purchase.date.desc()).limit(100).all()
    return jsonify([{
        'id': p.id,
        'date': p.date.strftime("%B %d, %Y"),
        'merchant': p.merchant,
        'amount': p.amount,
        'category': p.category,
    } for p in purchases])

@purchase_bp.route('/api/purchases', methods=['POST'])
def create_purchase():
    try:
        data = request.json
        
        # Validate required fields
        if not data.get('date') or not data.get('merchant') or not data.get('amount'):
            return jsonify({'success': False, 'error': 'Missing required fields: date, merchant, amount'})
        
        # Parse and validate date
        try:
            purchase_date = datetime.strptime(data['date'], "%B %d, %Y")
        except ValueError:
            return jsonify({'success': False, 'error': 'Invalid date format.'})
        
        # Validate amount
        try:
            amount = float(data['amount'])
            if amount <= 0:
                return jsonify({'success': False, 'error': 'Amount must be greater than 0'})
        except (ValueError, TypeError):
            return jsonify({'success': False, 'error': 'Invalid amount'})
        
        # Create the purchase
        purchase = Purchase(
            date=purchase_date,
            merchant=data['merchant'].strip(),
            amount=amount,
            category=data.get('category', 'Uncategorized'),
        )
        
        db.session.add(purchase)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'Purchase added successfully: {purchase.merchant} - ${purchase.amount:.2f}',
            'id': purchase.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@purchase_bp.route('/api/purchases/<int:purchase_id>', methods=['GET'])
def get_purchase(purchase_id):
    """Get a single purchase by ID"""
    purchase = Purchase.query.get_or_404(purchase_id)
    return jsonify({
        'id': purchase.id,
        'date': purchase.date.strftime("%B %d, %Y"),
        'merchant': purchase.merchant,
        'amount': purchase.amount,
        'category': purchase.category,
    })

@purchase_bp.route('/api/purchases/<int:purchase_id>', methods=['PUT'])
def update_purchase(purchase_id):
    purchase = Purchase.query.get_or_404(purchase_id)
    data = request.json
    
    if 'category' in data:
        purchase.category = data['category']
        
    db.session.commit()
    return jsonify({'success': True})

