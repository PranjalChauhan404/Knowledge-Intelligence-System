import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from app.services.s3_service import S3Service
from app.services.ingestion_service import IngestionService


upload_bp = Blueprint(
    "upload",
    __name__
)

s3_service = S3Service()
ingestion_service = IngestionService()

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".md"}

UPLOAD_FOLDER = "data/uploads"


def allowed_file(filename):
    extension = os.path.splitext(filename)[1].lower()
    return extension in ALLOWED_EXTENSIONS


@upload_bp.route("/upload", methods=["POST"])
def upload_document():

    if "file" not in request.files:
        return jsonify({
            "error": "No file provided"
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "error": "No file selected"
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            "error": "Only PDF, TXT, and Markdown files are supported"
        }), 400

    filename = secure_filename(file.filename)

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    local_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(local_path)

    s3_uri = s3_service.upload_file(
        local_path,
        filename
    )

    chunks_stored = ingestion_service.ingest(
        local_path,
        "default"
    )

    return jsonify({
        "message": "Document uploaded successfully",
        "filename": filename,
        "s3_uri": s3_uri,
        "chunks_stored": chunks_stored
    })