from flask import Blueprint, jsonify, request
from models.models import Budget


budget_bp = Blueprint("budgets", __name__)

@budget_bp.route('/budgets')
def budgets():
    budgets = Budget.query.all()
    return jsonify({"budgets":[b.to_dict() for b in budgets]})

@budget_bp.route('/api/budgets', methods=['POST'])
def create_budget():
    data = request.json
    budget = Budget(
        category=data['category'],
        monthly_limit=float(data['monthly_limit'])
    )
    db.session.add(budget)
    db.session.commit()
    return jsonify({'success': True, 'id': budget.id})

@budget_bp.route('/api/budgets/<int:budget_id>', methods=['DELETE'])
def delete_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    db.session.delete(budget)
    db.session.commit()
    return jsonify({'success': True})

