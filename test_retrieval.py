from app.services.retrieval_service import RetrievalService


retrieval = RetrievalService()

query = input("Ask a question: ")

results = retrieval.retrieve(
    query=query,
    collection_name="separation_test",
    top_k=3,
    similarity_threshold=1.6
)

print("\nRelevant results:")

for i, document in enumerate(results["documents"][0]):

    print(f"\n--- Result {i + 1} ---")
    print(document)

    print("Distance:", results["distances"][0][i])

    print("Metadata:", results["metadatas"][0][i])