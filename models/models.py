from db.db import db
from datetime import datetime

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    merchant = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), default='Uncategorized')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.Index('idx_unique_purchase', 'date', 'merchant', 'amount'),
    )

    def to_dict(self):
        return {
                "id":self.id,
                "date":self.date,
                "merchant":self.merchant,
                "amount":self.amount,
                "category":self.category
                }

class CategoryRule(db.Model):
    """Rules for auto-categorizing purchases"""
    id = db.Column(db.Integer, primary_key=True)
    merchant_pattern = db.Column(db.String(200), nullable=False)  # Merchant name pattern
    category = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.Integer, default=1)  # Higher priority rules are applied first
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.Index('idx_merchant_pattern', 'merchant_pattern'),
        db.Index('idx_category_rules', 'merchant_pattern'),
    )

    def to_dict(self):
        return {
                "id":self.id,
                "category":self.category,
                "merchant_pattern":self.merchant_pattern
                }

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), unique=True, nullable=False)
    monthly_limit = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
                "id":self.id,
                "category":self.category,
                "monthly_limit":self.monthly_limit
                }

