from flask import Flask, render_template
from app.routes.health import health_bp

def create_app():
    app = Flask(__name__, template_folder="../templates")

    app.register_blueprint(health_bp)

    @app.route("/")
    def home():
        return render_template("index.html")

    return app