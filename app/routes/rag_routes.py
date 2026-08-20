from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from app.services.rag_service import RAGService
from app.services.query_transformer import QueryTransformer
from app.models.api_models import QueryRequest
from app.utils.logger import logger


rag_bp = Blueprint("rag", __name__)

rag_service = RAGService()
query_transformer = QueryTransformer()


@rag_bp.route("/query", methods=["POST"])
def query():

    data = request.get_json(silent=True)

    if not data:
        logger.warning("Query request rejected: empty request body")

        return jsonify({
            "error": "Request body is required"
        }), 400


    try:

        query_request = QueryRequest(
            **data
        )

    except ValidationError as error:

        logger.warning(
            "Query request rejected: validation error"
        )

        return jsonify({
            "error": "Invalid request",
            "details": error.errors()
        }), 400


    transformed_query = query_transformer.transform(
        query_request.query
    )


    logger.info(
        "Query received | collection=%s | conversation_id=%s",
        query_request.collection,
        query_request.conversation_id or "default"
    )


    result = rag_service.answer_question(
        query=transformed_query,
        collection_name=query_request.collection,
        conversation_id=(
            query_request.conversation_id
            or "default"
        ),
        top_k=3,
        similarity_threshold=1.6
    )


    source_count = len(
        result.get("sources", [])
    )


    logger.info(
        "Query completed | collection=%s | sources=%s",
        query_request.collection,
        source_count
    )


    return jsonify({
        "answer": result["answer"],
        "sources": result["sources"],
        "conversation_id": (
            query_request.conversation_id
            or "default"
        )
    })