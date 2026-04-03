"""Health check and system status endpoints."""

from app import app, db
from flask import jsonify
from datetime import datetime
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for load balancers and monitoring.
    
    Returns the current health status of the application including
    database connectivity and system status.
    """
    try:
        # Check database connection
        db.session.execute(text('SELECT 1'))
        
        logger.info("Health check passed")
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "connected",
            "version": "1.0"
        }), 200
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}", exc_info=True)
        return jsonify({
            "status": "unhealthy",
            "error": "Database connection failed",
            "timestamp": datetime.utcnow().isoformat()
        }), 503


@app.route('/api/status', methods=['GET'])
def status():
    """Get detailed system status information."""
    try:
        db.session.execute(text('SELECT 1'))
        
        return jsonify({
            "status": "running",
            "timestamp": datetime.utcnow().isoformat(),
            "components": {
                "database": "operational",
                "api": "operational",
                "auth": "operational"
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Status check failed: {str(e)}", exc_info=True)
        return jsonify({
            "status": "degraded",
            "timestamp": datetime.utcnow().isoformat()
        }), 503
