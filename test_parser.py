from app.services.document_parser import DocumentParser

parser = DocumentParser()

files = [
    "data/test_documents/sample.pdf",
    "data/test_documents/sample.txt",
    "data/test_documents/sample.md"
]

for file in files:
    documents = parser.parse(file)

    print(f"\nFILE: {file}")
    print(f"Documents loaded: {len(documents)}")
    print("Text:", documents[0].page_content[:200])
    print("Metadata:", documents[0].metadata)