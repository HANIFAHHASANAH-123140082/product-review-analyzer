from pyramid.config import Configurator
from pyramid.events import BeforeRender
from waitress import serve
from database import DBSession, init_db
from config import Config

def add_cors_headers(event):
    """Add CORS headers to response"""
    response = event['request'].response
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'

def main():
    config = Configurator()
    
    config.add_request_method(
        lambda request: DBSession,
        'dbsession',
        reify=True
    )
    
    config.add_subscriber(add_cors_headers, BeforeRender)
    
    def options_view(request):
        request.response.headers['Access-Control-Allow-Origin'] = '*'
        request.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        request.response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return {}
    
    config.add_route('cors_options', '/{path:.*}', request_method='OPTIONS')
    config.add_view(options_view, route_name='cors_options', renderer='json')
    
    config.include('routes')
    config.scan('views')
    
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
    print(f"🌐 Server running at http://{Config.HOST}:{Config.PORT}")
    print("="*60)
    print("Press Ctrl+C to stop")
    print()
    
    serve(app, host=Config.HOST, port=Config.PORT)