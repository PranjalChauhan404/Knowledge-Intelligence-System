import os
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)


class DocumentParser:

    def parse(self, file_path):

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".pdf":
            loader = PyPDFLoader(file_path)

        elif extension in [".txt", ".md"]:
            loader = TextLoader(file_path, encoding="utf-8")

        else:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        return loader.load()