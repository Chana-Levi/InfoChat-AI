from flask import Flask
from authlib.integrations.flask_client import OAuth
from config import Config

oauth = OAuth()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    print(f"SECRET_KEY is set to: {app.config['SECRET_KEY']}") 

    oauth.init_app(app)

    oauth.register(
        name='google',
        client_id=Config.GOOGLE_CLIENT_ID,
        client_secret=Config.GOOGLE_CLIENT_SECRET,
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url="https://www.googleapis.com/oauth2/v1/",   #?????
        client_kwargs={'scope': 'profile email'}, #client_kwargs={'scope': 'openai profile email'},
        server_metadata_url=Config.GOOGLE_DISCOVERY_URL,
    )

    # Register blueprints
    from .routes.main_routes import main_bp
    from .routes.product_routes import product_bp
    from .routes.about_routes import about_bp
    from .routes.why_us_routes import why_us_bp
    from .routes.contact_routes import contact_bp  
    from .routes.chatbot_routes import chatbot_bp  
    from .routes.auth_routes import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(why_us_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(auth_bp)

    return app