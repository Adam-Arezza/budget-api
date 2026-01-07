from models.models import CategoryRule, Category

#categories
#Food & Dining
#Transportation
#Health & Wellness
#Shopping
#Groceries
#Services


def migrate_database(db):
    """Handle database migrations for existing installations"""
    # Check if the unique index exists
    inspector = db.inspect(db.engine)
    indexes = inspector.get_indexes('purchase')
    index_names = [index['name'] for index in indexes]
    
    if 'idx_unique_purchase' not in index_names:
        print("Creating unique index for purchases...")
        try:
            # Create the unique index
            db.engine.execute(
                'CREATE UNIQUE INDEX idx_unique_purchase ON purchase (date, merchant, amount)'
            )
            print("Unique index created successfully!")
        except Exception as e:
            print(f"Warning: Could not create unique index: {e}")
            print("Duplicate prevention will rely on application logic only.")
    
    # Check if CategoryRule table exists
    tables = inspector.get_table_names()
    if 'category_rule' not in tables:
        print("Creating CategoryRule table...")
        try:
            db.create_all()
            print("CategoryRule table created successfully!")
        except Exception as e:
            print(f"Warning: Could not create CategoryRule table: {e}")
    
    if Category.query.count() == 0:
        print("Creating default categories...")
        try:
            categories = [
                    Category(category='Food & Dining'),
                    Category(category='Transportation'),
                    Category(category='Services'),
                    Category(category='Shopping'),
                    Category(category='Groceries'),
                    Category(category='Health & Wellness'),
                    ]
            for category in categories:
                db.session.add(category)

            db.session.commit()
            print("created default categories.")
        except Exception as e:
            print(f"Warning: Could not create default categories: {e}")


    # Create some default category rules if none exist
    if CategoryRule.query.count() == 0:
        print("Creating default category rules...")
        try:
            default_rules = [
                CategoryRule(merchant_pattern='tim hortons', category='Food & Dining', priority=10),
                CategoryRule(merchant_pattern='starbucks', category='Food & Dining', priority=10),
                CategoryRule(merchant_pattern='subway', category='Food & Dining', priority=10),
                CategoryRule(merchant_pattern='mcdonalds', category='Food & Dining', priority=10),
                CategoryRule(merchant_pattern='shell', category='Transportation', priority=10),
                CategoryRule(merchant_pattern='esso', category='Transportation', priority=10),
                CategoryRule(merchant_pattern='uber', category='Transportation', priority=10),
                CategoryRule(merchant_pattern='walmart', category='Shopping', priority=10),
                CategoryRule(merchant_pattern='costco', category='Shopping', priority=10),
                CategoryRule(merchant_pattern='amazon', category='Shopping', priority=10),
                CategoryRule(merchant_pattern='rogers', category='Bills & Utilities', priority=10),
                CategoryRule(merchant_pattern='bell', category='Bills & Utilities', priority=10),
            ]
            
            for rule in default_rules:
                db.session.add(rule)
            
            db.session.commit()
            print(f"Created {len(default_rules)} default category rules!")
        except Exception as e:
            print(f"Warning: Could not create default rules: {e}")

    
