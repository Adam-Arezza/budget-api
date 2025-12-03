import os
import sys
from dotenv import load_dotenv
from pathlib import Path
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date
from db.db import db
from db.migrations import migrate_database
from services.sync_service import SyncService
from routes.purchases import purchase_bp
from routes.budget import budget_bp
from routes.categories import category_bp
from routes.dashboard import dashboard_bp

load_dotenv()
db_path = ""

if sys.platform == "win32":
    db_path = str(Path.home())+os.getenv("WINDOWS_PATH")
else:
    db_path = str(Path.home())+os.getenv("LINUX_PATH")

db_dir = Path(db_path)
db_dir.parent.mkdir(parents=True, exist_ok=True)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    db.init_app(app)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(purchase_bp)
    app.register_blueprint(budget_bp)
    app.register_blueprint(category_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        sync_service = SyncService(db)
        db.create_all()
        migrate_database(db)
        sync_service.sync()
    app.run(debug=True, host='0.0.0.0', port=5000)
