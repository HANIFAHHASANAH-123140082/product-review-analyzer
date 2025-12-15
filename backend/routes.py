def includeme(config):
    """Add routes to the application"""
    config.add_route('home', '/')
    config.add_route('analyze_review', '/api/analyze-review')
    config.add_route('get_reviews', '/api/reviews')