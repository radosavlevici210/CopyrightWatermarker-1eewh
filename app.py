#!/usr/bin/env python3
"""
Quantum Security System - Main Application
Copyright © 2025 Ervin Remus Radosavlevici
Official Owner: Ervin Remus Radosavlevici
Contact: radosavlevici210@icloud.com
Official Timestamp: 2025-01-20 12:00:00 UTC
Private and Public Repository Rights Reserved
Licensed under MIT License with additional copyright protections
All rights reserved.
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import logging
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "quantum-security-default-key-2025")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///quantum_security.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

with app.app_context():
    try:
        # Import models first
        import models  # noqa: F401

        # Create all database tables
        db.create_all()
        logging.info("Database tables created successfully")

        # Initialize quantum security database components
        from quantum_security import init_db_components
        init_db_components()

        # Import routes after database setup
        import routes  # noqa: F401

    except Exception as e:
        logging.error(f"Database initialization error: {e}")
        # Don't raise the error, continue with limited functionality
        print("Continuing with limited database functionality")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)