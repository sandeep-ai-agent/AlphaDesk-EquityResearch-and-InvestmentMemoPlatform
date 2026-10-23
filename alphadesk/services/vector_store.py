'''
1. Read teh saved Embedding records
2. validate each chunks text and Citation Fields
3. check the model, vector size , numerical values
4. Convert each record to Qdrant Point
5. Connect to Qdrant
6. Create Collection if needed
7. Upload points in small batches
8. Return the number submitted

'''

import json
from uuid import NAMESPACE_URL, uuid5 

from qdrant_client import QdrantClient, models
# Import Database Client and its models

from alphadesk.contracts.chunks import EvidenceChunk

MODEL_NAME = "BAAI/bge-small-en-v1.5"
VECTOR_SIZE = 384
COLLECTION_NAME = "alphadesk_bge_small_en_v1_5"

def index_embeddings(embedding_file: str) -> int:
    """ Read saved Embeddings and store them in Qdrant """

    # Open the Exact File name 
    with open(embedding_file, encoding="utf-8") as source:
        records = [json.loads(line) for line in source]

        if not records:
            raise ValueError("embedding File is Empty")

        points = [] #Collect Database Records for this Report

        # Our chunk IDs contain text that Qdrant cannot use directly as point IDs. 
        # This converts them into an accepted format and ensures
        # uploading the same chunk again updates its existing point instead of adding a duplicate.

        # this code creates unique , ID for each passage stored in Qdrant
        for record in records:
            point_id = str(
                uuid5(
                    NAMESPACE_URL, # pre dffined value used buy uuid5(). no URL
                    f"{MODEL_NAME}:{record['chunk_id']}" # Chunk_id coming from PAgeEvidence Class
                )
            )

            # Now also retain passage and source reference form record

            payload = {"chunk_id": record["chunk_id"],
                       "document_id": record["document_id"],
                       "pdf_page_number": record["pdf_page_number"],
                       "text": record["text"],
                       "embedding_model": record["embedding_model"]
            }

            # So finally Combine the ID , Vector , Payload into one point
            point = models.PointStruct(
                id=point_id,
                vector=record["embedding"],
                payload=payload
            )

            points.append(point)

            # Now everything is ready and now we will put it in Qdrant Database

            #connect to Qdrant Server ( running on our local here )
        client = QdrantClient(url="http://127.0.0.1:6333")

                # Create Collection on First Run
        if not client.collection_exists(COLLECTION_NAME):
                    client.create_collection(
                        collection_name=COLLECTION_NAME,
                        vectors_config=models.VectorParams(
                            size=VECTOR_SIZE,
                            distance=models.Distance.COSINE
                        ),
                    )

            # Else Upsert in batches
        for start in range(0, len(points), 64):
            # Select the next group of up to 64 points.
            batch = points[start:start + 64]
            client.upsert(
                    collection_name=COLLECTION_NAME,
                    points=batch,
                    wait=True
                )
            client.close()
            return len(points)







