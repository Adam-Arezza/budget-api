from datetime import datetime, timedelta
from services.imap_client import EmailClient
from services.categorize import auto_categorize_purchase
from models.models import Purchase

class SyncService:
    def __init__(self, db):
        self.client = EmailClient()
        self.db = db

    def sync(self):
        last_purchase = Purchase.query.order_by(Purchase.date.desc()).first()
        since_date = None
        if last_purchase:
            # Get emails from 1 day before the last purchase to ensure we don't miss any
            since_date = last_purchase.date - timedelta(days=1)
        
        purchases = self.client.get_purchase_notifications(since_date)
        new_purchases = 0
        skipped_purchases = 0
        
        for purchase_data in purchases:
            existing = Purchase.query.filter(
                Purchase.date == datetime.strptime(purchase_data['date'], "%B %d, %Y"),
                Purchase.merchant == purchase_data['merchant'],
                Purchase.amount == purchase_data['amount'],
            ).first()
            
            if not existing:
                # Auto-categorize the purchase
                auto_category = auto_categorize_purchase(
                    purchase_data['merchant'], 
                )
                
                purchase = Purchase(
                    date=datetime.strptime(purchase_data['date'], "%B %d, %Y"),
                    merchant=purchase_data['merchant'],
                    amount=purchase_data['amount'],
                    category=auto_category
                )
                self.db.session.add(purchase)
                new_purchases += 1
            else:
                skipped_purchases += 1
        self.db.session.commit()
        return new_purchases,skipped_purchases

