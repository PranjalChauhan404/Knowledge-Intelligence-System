import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()


class EmbeddingService:

    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def embed_documents(self, documents):
        return self.embeddings.embed_documents(documents)

    def embed_query(self, query):
        return self.embeddings.embed_query(query)