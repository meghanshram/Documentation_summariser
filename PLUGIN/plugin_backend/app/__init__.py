from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True  # Optional: Pretty-print JSON responses

    # Import routes
    from app.routes import bp
    app.register_blueprint(bp)

    return app
