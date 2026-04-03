import os
from sqlalchemy.pool import QueuePool


class Config:
    """Base configuration for the application."""
    
    # Security - Prevent hardcoded defaults in production
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        SECRET_KEY = "dev-secret-key"  # Dev only
    
    DEBUG = False

    # Database settings
    DB_HOST = os.environ.get("MYSQL_HOST", "localhost")
    DB_PORT = int(os.environ.get("MYSQL_PORT", 3306))
    DB_USER = os.environ.get("MYSQL_USER", "root")
    DB_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
    DB_NAME = os.environ.get("MYSQL_DATABASE", "surplusx")
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Set to True for SQL debugging
    
    # Database connection pooling and optimization
    SQLALCHEMY_ENGINE_OPTIONS = {
        'poolclass': QueuePool,
        'pool_size': 10,
        'max_overflow': 20,
        'pool_recycle': 3600,  # Recycle connections every hour
        'pool_pre_ping': True,  # Verify connections before use
    }
    
    # JWT Configuration - Prevent hardcoded defaults in production
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    if not JWT_SECRET_KEY:
        JWT_SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", 86400))  # 24 hours
    JWT_ALGORITHM = "HS256"
    
    # CORS
    ORIGINS = os.environ.get("ORIGINS", "http://localhost:3000")
    
    # Request size limits (prevent DoS)
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB max request size
    JSON_SORT_KEYS = False
    
    # Security headers
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    ORIGINS = "http://localhost:3000"
    SESSION_COOKIE_SECURE = False  # Allow HTTP in development


class TestingConfig(Config):
    """Testing configuration uses SQLite."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ECHO = False
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour for testing
    
    # SQLite doesn't need connection pooling
    SQLALCHEMY_ENGINE_OPTIONS = {}


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    ORIGINS = os.environ.get("ORIGINS", "http://localhost:3000")
    SESSION_COOKIE_SECURE = True  # HTTPS only
    
    # Validate secrets are set in production
    @classmethod
    def validate(cls):
        """Validate production configuration is correct."""
        if os.environ.get("FLASK_ENV") == "production":
            if not os.environ.get("SECRET_KEY"):
                raise ValueError("SECRET_KEY must be set in production")
            if not os.environ.get("JWT_SECRET_KEY"):
                raise ValueError("JWT_SECRET_KEY must be set in production")


# Validate production config on import if needed
if os.environ.get("FLASK_ENV") == "production":
    ProductionConfig.validate()
    
    def __init__(self):
        # Require SECRET_KEY in production
        if not os.environ.get("SECRET_KEY"):
            raise ValueError("SECRET_KEY environment variable must be set in production")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
