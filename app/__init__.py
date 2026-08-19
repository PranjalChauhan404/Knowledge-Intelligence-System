from flask import Flask, render_template
from app.routes.health import health_bp
from app.routes.rag_routes import rag_bp
from app.routes.upload_routes import upload_bp
from app.routes.document_routes import document_bp
from app.routes.collection_routes import collection_bp      
from app.routes.config_routes import config_bp          

def create_app():
    app = Flask(
        __name__,
        template_folder="../templates"
    )

    app.register_blueprint(health_bp)
    app.register_blueprint(rag_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(document_bp)
    app.register_blueprint(collection_bp)
    app.register_blueprint(config_bp)
    @app.route("/")
    def home():
        return render_template("index.html")

    return app