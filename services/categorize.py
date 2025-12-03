from models.models import CategoryRule


def auto_categorize_purchase(merchant):
    """Automatically categorize a purchase based on rules and patterns"""
    if not merchant:
        return 'Uncategorized'
    
    # Get all category rules ordered by priority
    rules = CategoryRule.query.order_by(CategoryRule.priority.desc()).all()
    
    for rule in rules:
        # Check if merchant matches the pattern
        if rule.merchant_pattern.lower() in merchant.lower():
            # If description pattern is specified, check that too
            return rule.category
    
    # If no rules match, try to infer from common patterns
    merchant_lower = merchant.lower()
    
    # Food & Dining
    food_keywords = ['restaurant', 'cafe', 'coffee', 'pizza', 'burger', 'subway', 'mcdonalds', 'tim hortons', 'starbucks']
    if any(keyword in merchant_lower for keyword in food_keywords):
        return 'Food & Dining'
    
    # Transportation
    transport_keywords = ['uber', 'lyft', 'taxi', 'gas', 'shell', 'esso', 'petro', 'parking', 'transit', 'go transit']
    if any(keyword in merchant_lower for keyword in transport_keywords):
        return 'Transportation'
    
    # Shopping
    shopping_keywords = ['walmart', 'costco', 'amazon', 'best buy', 'canadian tire', 'home depot', 'lowe']
    if any(keyword in merchant_lower for keyword in shopping_keywords):
        return 'Shopping'
    
    # Entertainment
    entertainment_keywords = ['netflix', 'spotify', 'movie', 'theatre', 'cinema', 'game', 'playstation', 'xbox']
    if any(keyword in merchant_lower for keyword in entertainment_keywords):
        return 'Entertainment'
    
    # Bills & Utilities
    bills_keywords = ['hydro', 'electric', 'water', 'gas', 'internet', 'phone', 'rogers', 'bell', 'telus']
    if any(keyword in merchant_lower for keyword in bills_keywords):
        return 'Bills & Utilities'
    
    # Health & Fitness
    health_keywords = ['pharmacy', 'shoppers', 'rexall', 'gym', 'fitness', 'medical', 'dental']
    if any(keyword in merchant_lower for keyword in health_keywords):
        return 'Health & Fitness'
    
    return 'Uncategorized'

