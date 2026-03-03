from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
from sqlalchemy import text
from models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)  

    @app.route('/test-db')
    def test_db():
        try:
            db.session.execute(text('SELECT 1'))
            return jsonify({'status': 'DB Connected'})
        except Exception as e:
            return jsonify({'status': 'DB Connection failed', 'error': str(e)})
    
    from routes.sales import sales_bp
    from routes.reports import reports_bp
    from routes.analytics import analytics_bp
    
    app.register_blueprint(sales_bp)   
    app.register_blueprint(reports_bp)
    app.register_blueprint(analytics_bp) 
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)