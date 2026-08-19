from flask import Blueprint, request, jsonify
from app.services.rag_service import RAGService


rag_bp = Blueprint("rag", __name__)

rag_service = RAGService()


@rag_bp.route("/query", methods=["POST"])
def query():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    query_text = data.get("query")

    if not query_text:
        return jsonify({
            "error": "Query is required"
        }), 400

    collection_name = data.get(
        "collection",
        "default"
    )

    conversation_id = data.get(
        "conversation_id",
        "default"
    )

    result = rag_service.answer_question(
        query=query_text,
        collection_name=collection_name,
        conversation_id=conversation_id,
        top_k=3,
        similarity_threshold=1.6
    )

    return jsonify({
        "answer": result["answer"],
        "sources": result["sources"],
        "conversation_id": conversation_id
    })