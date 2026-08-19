from flask import Blueprint, jsonify


config_bp = Blueprint("config", __name__)


@config_bp.route("/config", methods=["GET"])
def get_config():

    return jsonify({
        "collection": "default",
        "top_k": 3,
        "similarity_threshold": 1.6,
        "allowed_file_types": [
            ".pdf",
            ".txt",
            ".md"
        ]
    })