import os
from datetime import datetime

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from app.services.s3_service import S3Service
from app.services.ingestion_service import IngestionService
from app.services.metadata_service import MetadataService
from app.services.document_registry_service import DocumentRegistryService


upload_bp = Blueprint("upload", __name__)

s3_service = S3Service()
ingestion_service = IngestionService()
metadata_service = MetadataService()
registry_service = DocumentRegistryService()

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

    # 1. Store raw document in S3
    s3_uri = s3_service.upload_file(
        local_path,
        filename
    )

    # 2. Process document and store chunks in ChromaDB
    chunks_stored = ingestion_service.ingest(
        local_path,
        "default"
    )

    # 3. Create stable document ID
    document_id = metadata_service.create_document_id(
        local_path
    )

    # 4. Register document
    registry_service.add_document({
        "document_id": document_id,
        "filename": filename,
        "file_type": os.path.splitext(filename)[1].lower(),
        "upload_date": datetime.now().isoformat(),
        "collection": "default",
        "s3_uri": s3_uri,
        "status": "indexed",
        "chunk_count": chunks_stored
    })

    # 5. Return API response
    return jsonify({
        "message": "Document uploaded successfully",
        "document_id": document_id,
        "filename": filename,
        "s3_uri": s3_uri,
        "chunks_stored": chunks_stored,
        "status": "indexed"
    })