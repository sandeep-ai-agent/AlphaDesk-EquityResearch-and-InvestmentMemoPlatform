'''
1. It will load the chunks
2. load the embedding model
3. check every chunk fits models input limit
4. convert chunk into vectors
5. Save each vector alongside its orignal chunk Information

'''
import json
from pathlib import Path

from sentence_transformers import SentenceTransformer
# Embedding Model

from alphadesk.contracts.chunks import EvidenceChunk

MODEL_NAME = "BAAI/bge-small-en-v1.5"

def embed_chunks(chunks_path: Path) -> Path:
    output_path = chunks_path.with_name(f"{chunks_path.stem}_embeddings.jsonl")

    if output_path.exists():
        raise ValueError(f"Output already exists:{output_path}")

    with chunks_path.open(encoding="utf-8") as source:
        # Open chunks file already created in last step
        chunks = [EvidenceChunk.model_validate_json(line) for line in source] # For each chunk record

        if not chunks:
            raise ValueError("Chunk File is Empty")

        model = SentenceTransformer(
            MODEL_NAME,
            device="cpu",
        )

        # Extract passage text as it is for chunks
        texts = [chunk.text for chunk in chunks]

        vectors = model.encode(
                texts,
                batch_size=8,
                normalize_embeddings=True,
                show_progress_bar=True,
                convert_to_numpy=True,
        )

        with output_path.open("x", encoding="utf-8") as output:
            for chunk, vector in zip(chunks, vectors, strict=True): # Pair chenku with its vector
                record = chunk.model_dump() # Keep original passage and citation fields
                record["embedding_model"] = MODEL_NAME # Record which model name create vcector
                record["normalized"] = True 
                record["embedding"] = vector.tolist()  # Convert NumPy Vector into JSON-compatible List , so creating Vectors here

                output.write(json.dumps(record)+ "\n")

        print(f"Embedded {len(chunks)} chunks.")
        print(f"Vector Dimensions: {vectors.shape[1]}")

        return output_path




        






