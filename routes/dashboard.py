from flask import Blueprint, jsonify, request
from models.models import Purchase 
from db.db import db
from services.categorize import auto_categorize_purchase

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route('/')
def dashboard():
    # Get current month's purchases
    current_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    purchases = Purchase.query.filter(Purchase.date >= current_month).order_by(Purchase.date.desc()).all()
    # Calculate totals
    total_spent = sum(p.amount for p in purchases)
    
    # Get category breakdown
    categories = db.session.query(Purchase.category, db.func.sum(Purchase.amount)).filter(
        Purchase.date >= current_month
    ).group_by(Purchase.category).all()
    
    # Get recent purchases for the table
    recent_purchases = Purchase.query.order_by(Purchase.date.desc()).limit(10).all()
    day = date.today().day

    dashboard_data = {
            "purchases": purchases,
            "total_spent": total_spent,
            "categories": categories,
            "recent_purchases": recent_purchases,
            "day": day
            }

    return jsonify(dashboard_data)

@dashboard_bp.route('/api/bulk-categorize', methods=['POST'])
def bulk_categorize():
    """Apply category to multiple purchases"""
    try:
        data = request.json
        purchase_ids = data.get('purchase_ids', [])
        category = data.get('category')
        
        if not purchase_ids or not category:
            return jsonify({'success': False, 'error': 'Missing purchase IDs or category'})
        
        # Update all specified purchases
        updated_count = Purchase.query.filter(Purchase.id.in_(purchase_ids)).update(
            {'category': category}, 
            synchronize_session=False
        )
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'Updated {updated_count} purchases with category: {category}'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@dashboard_bp.route('/api/auto-categorize-all', methods=['POST'])
def auto_categorize_all():
    try:
        # Get all uncategorized purchases
        uncategorized = Purchase.query.filter(
            Purchase.category.in_(['Uncategorized', ''])
        ).all()
        
        updated_count = 0
        for purchase in uncategorized:
            new_category = auto_categorize_purchase(purchase.merchant)
            if new_category != 'Uncategorized':
                purchase.category = new_category
                updated_count += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'Auto-categorized {updated_count} purchases'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
