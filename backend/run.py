from app import app, db
import logging
import sys
import os
import time
from sqlalchemy import text

# Setup logging (use stdout only for development/Docker)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def wait_for_db(max_retries=30, retry_delay=2):
    """Wait for database to be ready before proceeding"""
    logger.info("Waiting for database to be ready...")
    
    for attempt in range(max_retries):
        try:
            with app.app_context():
                # Test database connection
                db.session.execute(text('SELECT 1'))
                db.session.commit()
                logger.info("✓ Database is ready!")
                return True
        except Exception as e:
            attempt_num = attempt + 1
            logger.warning(f"Database connection attempt {attempt_num}/{max_retries} failed: {str(e)[:100]}")
            
            if attempt_num < max_retries:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error("Failed to connect to database after maximum retries")
                return False
    
    return False


if __name__ == '__main__':
    # Wait for database to be ready
    if not wait_for_db():
        logger.error("Cannot proceed without database connection")
        sys.exit(1)
    
    # Auto-initialize database on startup
    try:
        with app.app_context():
            db.create_all()
            logger.info("✓ Database tables initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database tables: {str(e)}")
        sys.exit(1)
    
    logger.info("Starting Flask application on 0.0.0.0:5000")
    # Use DEBUG environment variable or default to False for production safety
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)