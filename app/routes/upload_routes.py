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

    # ------------------------------------------
    # 1. Validate request
    # ------------------------------------------

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


    # ------------------------------------------
    # 2. Save uploaded file temporarily
    # ------------------------------------------

    filename = secure_filename(file.filename)

    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )

    local_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(local_path)


    # ------------------------------------------
    # 3. Create stable document ID
    # ------------------------------------------

    document_id = metadata_service.create_document_id(
        local_path
    )


    # ------------------------------------------
    # 4. Idempotency check
    # ------------------------------------------

    existing_document = registry_service.get_document(
        document_id
    )

    if existing_document:

        # Remove temporary uploaded file
        if os.path.exists(local_path):
            os.remove(local_path)

        return jsonify({
            "error": "Document already exists",
            "document_id": document_id,
            "filename": existing_document["filename"]
        }), 409


    # ------------------------------------------
    # 5. Store raw document in S3
    # ------------------------------------------

    try:

        s3_uri = s3_service.upload_file(
            local_path,
            filename
        )


        # ------------------------------------------
        # 6. Process document and store chunks
        # ------------------------------------------

        chunks_stored = ingestion_service.ingest(
            local_path,
            "default"
        )


        # ------------------------------------------
        # 7. Register document
        # ------------------------------------------

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


        # ------------------------------------------
        # 8. Return successful response
        # ------------------------------------------

        return jsonify({
            "message": "Document uploaded successfully",
            "document_id": document_id,
            "filename": filename,
            "s3_uri": s3_uri,
            "chunks_stored": chunks_stored,
            "status": "indexed"
        })


    except Exception as error:

        # ------------------------------------------
        # 9. Cleanup if ingestion fails
        # ------------------------------------------

        return jsonify({
            "error": "Document upload failed",
            "details": str(error)
        }), 500


    finally:

        # ------------------------------------------
        # 10. Remove local temporary file
        # ------------------------------------------

        if os.path.exists(local_path):
            os.remove(local_path)