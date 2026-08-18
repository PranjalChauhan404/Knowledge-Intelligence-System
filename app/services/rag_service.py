from app.services.retrieval_service import RetrievalService
from app.services.llm_service import LLMService
from app.services.conversation_service import ConversationService


class RAGService:

    def __init__(self):
        self.retrieval_service = RetrievalService()
        self.llm_service = LLMService()
        self.conversation_service = ConversationService()

    def answer_question(
        self,
        query,
        collection_name,
        conversation_id="default",
        top_k=5,
        similarity_threshold=1.6
    ):

        history = self.conversation_service.get_history(
            conversation_id
        )

        results = self.retrieval_service.retrieve(
            query=query,
            collection_name=collection_name,
            top_k=top_k,
            similarity_threshold=similarity_threshold
        )

        context_parts = []

        for document in results["documents"][0]:
            context_parts.append(document)

        context = "\n\n".join(context_parts)

        history_text = "\n".join(
            f"{message['role']}: {message['content']}"
            for message in history
        )

        prompt = f"""
You are a Knowledge Intelligence assistant.

Answer the user's question using ONLY the provided document context.

Use the conversation history to understand follow-up questions.

If the answer cannot be found in the document context, say:
"I couldn't find that information in the uploaded documents."

Do not invent or assume information.

Conversation History:
{history_text}

Document Context:
{context}

User Question:
{query}

Answer:
"""

        answer = self.llm_service.generate_response(prompt)

        self.conversation_service.add_message(
            conversation_id,
            "user",
            query
        )

        self.conversation_service.add_message(
            conversation_id,
            "assistant",
            answer
        )

        sources = []

        for metadata in results["metadatas"][0]:
            sources.append({
                "document_id": metadata.get("document_id"),
                "filename": metadata.get("filename"),
                "chunk_id": metadata.get("chunk_id"),
                "source": metadata.get("source")
            })

        return {
            "answer": answer,
            "sources": sources
        }