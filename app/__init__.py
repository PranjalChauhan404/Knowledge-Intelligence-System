from flask import Flask, render_template
from app.routes.health import health_bp
from app.routes.rag_routes import rag_bp
from app.routes.upload_routes import upload_bp

def create_app():
    app = Flask(
        __name__,
        template_folder="../templates"
    )

    app.register_blueprint(health_bp)
    app.register_blueprint(rag_bp)
    app.register_blueprint(upload_bp)
    @app.route("/")
    def home():
        return render_template("index.html")

    return app