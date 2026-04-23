from flask import Flask, jsonify

from .config import Config
from .docs import docs
from .routes import api


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    app.json.sort_keys = False

    @app.get("/")
    def root():
        return jsonify(
            {
                "service": "german-scenario-backend",
                "status": "ok",
                "docs": "/docs",
            }
        )

    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(docs)
    return app
