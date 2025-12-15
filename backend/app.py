from pyramid.config import Configurator
from pyramid.response import Response
from waitress import serve
from database import DBSession, init_db
from config import Config

def add_cors_to_response(event):
    """Add CORS headers to all responses"""
    def cors_callback(request, response):
        response.headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        })
    event.request.add_response_callback(cors_callback)

def main():
    """Main application entry point"""
    config = Configurator()
    
    # Add database session to request
    config.add_request_method(
        lambda request: DBSession,
        'dbsession',
        reify=True
    )
    
    # Add CORS subscriber
    config.add_subscriber(add_cors_to_response, 'pyramid.events.NewRequest')
    
    # Handle OPTIONS preflight requests
    def options_view(context, request):
        return Response(
            status=200,
            headers={
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            }
        )
    
    config.add_route('options_route', '/{path:.*}', request_method='OPTIONS')
    config.add_view(options_view, route_name='options_route')
    
    # Include routes
    config.include('routes')
    
    # Scan for views
    config.scan('views')
    
    # Create WSGI application
    app = config.make_wsgi_app()
    
    return app

if __name__ == '__main__':
    print("="*60)
    print("🚀 Starting Product Review Analyzer Backend")
    print("="*60)
    
    print("📊 Initializing database...")
    try:
        init_db()
        print("✅ Database ready!")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        print("Make sure PostgreSQL is running and credentials are correct")
        exit(1)
    
    app = main()
    
    # Print routes for debugging
    print("="*60)
    print(f"🌐 Server: http://{Config.HOST}:{Config.PORT}")
    print("="*60)
    print("Routes registered:")
    print("  - GET  /")
    print("  - POST /api/analyze-review")
    print("  - GET  /api/reviews")
    print("="*60)
    print("Press Ctrl+C to stop")
    print()
    
    serve(app, host=Config.HOST, port=Config.PORT)