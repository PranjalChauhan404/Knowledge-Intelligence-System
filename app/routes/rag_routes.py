from flask import Blueprint, request, jsonify
from app.services.rag_service import RAGService


rag_bp = Blueprint(
    "rag",
    __name__
)

rag_service = RAGService()


@rag_bp.route("/ask", methods=["POST"])
def ask_question():

    data = request.get_json()

    query = data.get("query")
    collection_name = data.get(
        "collection_name",
        "default"
    )
    conversation_id = data.get(
        "conversation_id",
        "default"
    )

    if not query:
        return jsonify({
            "error": "Query is required"
        }), 400

    result = rag_service.answer_question(
        query=query,
        collection_name=collection_name,
        conversation_id=conversation_id,
        top_k=3,
        similarity_threshold=1.6
    )

    return jsonify(result)