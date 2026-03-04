from flask import Flask
from config import Config
from extensions import jwt, db
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.sales_routes import sales_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    jwt.init_app(app)
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(sales_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api")

    @app.route("/")
    def home():
        return "Backend is running successfully"

    # Create tables if not exist
    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)