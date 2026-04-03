from app import app, db
import logging
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    # Auto-initialize database on startup
    with app.app_context():
        db.create_all()
        logger.info("Database tables initialized")
    
    logger.info("Starting Flask application on 0.0.0.0:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)