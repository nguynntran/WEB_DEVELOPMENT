import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key used to encrypt sessions and cookies
    # Get from environment variable, otherwise use default
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database location: SQLite file stored in database/tournament.db
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database', 'tournament.db')
    
    # Turn off modification tracking to save memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    # Enable debug mode: auto-reload on code changes,
    DEBUG = True
    
    # Print all SQL queries 
    SQLALCHEMY_ECHO = True  

class ProductionConfig(Config):
    # Disable debug mode for security when deploying to real server
    DEBUG = False

# Dictionary to easily switch between different configurations
config = {
    'development': DevelopmentConfig,  # For local development
    'production': ProductionConfig,     # For live deployment
    'default': DevelopmentConfig        # Default configuration
}