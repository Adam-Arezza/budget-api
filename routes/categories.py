from flask import Blueprint, jsonify, request
from models.models import CategoryRule, Category


category_bp = Blueprint("category_rules", __name__)

@category_bp.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{"id":category.id,"category":category.category} for category in categories])

@category_bp.route('/api/category-rules', methods=['GET'])
def get_category_rules():
    """Get all category rules"""
    rules = CategoryRule.query.order_by(CategoryRule.priority.desc()).all()
    return jsonify([{
        'id': rule.id,
        'merchant_pattern': rule.merchant_pattern,
        'category': rule.category,
        'priority': rule.priority
    } for rule in rules])

@category_bp.route('/api/category-rules', methods=['POST'])
def create_category_rule():
    try:
        data = request.json
        rule = CategoryRule(
            merchant_pattern=data['merchant_pattern'],
            category=data['category'],
            priority=data.get('priority', 1)
        )
        db.session.add(rule)
        db.session.commit()
        return jsonify({'success': True, 'id': rule.id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@category_bp.route('/api/category-rules/<int:rule_id>', methods=['DELETE'])
def delete_category_rule(rule_id):
    """Delete a category rule"""
    try:
        rule = CategoryRule.query.get_or_404(rule_id)
        db.session.delete(rule)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

