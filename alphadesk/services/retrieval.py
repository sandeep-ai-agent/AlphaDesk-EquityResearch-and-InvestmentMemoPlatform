'''
We’ll write one function, search_passages(), which:
1. Loads our embedding model.
2. Converts the question into a vector.
3. Searches the existing Qdrant collection.
4. Returns the matching points, including their text and page references.
We reuse the constants from vector_store.py so indexing and searching use the same settings.

'''

from alphadesk.services.vector_store import index_embeddings, COLLECTION_NAME, MODEL_NAME
from qdrant_client import QdrantClient # To connect ot qdrant
from sentence_transformers import SentenceTransformer  # To Embed Question/Query

def search_passages(question: str, top_k: int = 3):

    # Load the same model used for embedding
    model = SentenceTransformer(MODEL_NAME, device="cpu")

    query_text = ("Represent this sentence for searching the relevant passages: " + question)

    # eMbed the query to vectors
    query_vector = model.encode(
        query_text,
        normalize_embeddings=True,
        convert_to_numpy=True
    )

    # connect to Qdrant server
    client = QdrantClient(url="http://127.0.0.1:6333")

    # Search the Collectiosn using the Question
    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector.tolist(),  #COnvert numpy values to List as it will be like [[]]
        limit=top_k,
        with_payload=True,
        with_vectors=False,
    )

    client.close
    return response.points
'''
 Lets Execute this File Directly for now
if __name__ == "__main__":
    # Ask user to enter a question
    question = input("Enter your question")

    results = search_passages(question, top_k=3)

    # Numbering of returned passages
    for position,result in enumerate(results,start=1):
        # Read passage metadata
        passage=result.payload

        # show result number and similarity to 3 decimal palces
        print(f"\n Result {position} | Similarity : {result.score:.3f}")

        # show which document and physical PDF page it came from
        print(f"Document: {passage['document_id']}")
        print(f"PDF Page : {passage['pdf_page_number']}")

        # Show Complete Passage
        print(passage["text"])
'''








