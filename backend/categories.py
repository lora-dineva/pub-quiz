"""
Categories and subcategories configuration for the Pub Quiz application.
"""

# Dictionary of question categories and their subcategories
QUIZ_CATEGORIES = {
    "History": ["Ancient", "Medieval", "Modern", "World Wars"],
    "Music": ["Pop", "Rock", "Classical", "Jazz", "90s"],
    "Movies": ["Action", "Comedy", "Drama", "Horror"],
    "Sports": ["Football", "Basketball", "Olympics", "Tennis"],
    "Science": ["Physics", "Chemistry", "Biology", "Astronomy"],
    "Literature": ["Novels", "Poetry", "Plays", "Authors"],
    "Geography": ["Countries", "Capitals", "Flags", "Mountains"],
    "Pop Culture": ["Celebrities", "Memes", "TV Shows", "Trends"],
    "Technology": ["Computers", "AI", "Internet", "Gadgets"]
}


def get_all_categories():
    """Return a list of all available categories."""
    return list(QUIZ_CATEGORIES.keys())


def get_subcategories(category):
    """
    Get subcategories for a given category.
    
    Args:
        category (str): The main category name
        
    Returns:
        list: List of subcategories or empty list if category not found
    """
    return QUIZ_CATEGORIES.get(category, [])


def is_valid_category(category):
    """Check if a category is valid."""
    return category in QUIZ_CATEGORIES


def is_valid_subcategory(category, subcategory):
    """Check if a subcategory is valid for the given category."""
    if not is_valid_category(category):
        return False
    return subcategory in QUIZ_CATEGORIES[category]


def get_category_subcategory_pairs():
    """
    Get all valid category-subcategory pairs.
    
    Returns:
        list: List of tuples (category, subcategory)
    """
    pairs = []
    for category, subcategories in QUIZ_CATEGORIES.items():
        for subcategory in subcategories:
            pairs.append((category, subcategory))
    return pairs


# For easy importing
__all__ = [
    'QUIZ_CATEGORIES',
    'get_all_categories',
    'get_subcategories',
    'is_valid_category',
    'is_valid_subcategory',
    'get_category_subcategory_pairs'
] 