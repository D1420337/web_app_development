from flask import Flask
import os
import sqlite3

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['DATABASE'] = os.path.join(app.instance_path, 'database.db')

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize DB function
    def init_db():
        db = sqlite3.connect(app.config['DATABASE'])
        with app.open_resource('../database/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
    
    import click
    @app.cli.command('init-db')
    def init_db_command():
        """Clear the existing data and create new tables."""
        init_db()
        click.echo('Initialized the database.')

    # Register Blueprints
    from .routes.auth import auth_bp
    from .routes.book import book_bp
    from .routes.user import user_bp
    from .routes.message import message_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(book_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(message_bp)

    return app
