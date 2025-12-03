import os
from openai import OpenAI
from src.services.logger_service import logger

GEMINI_EMBEDDING_API_KEY = os.getenv("GEMINI_EMBEDDING_API_KEY")

client = OpenAI(
    api_key=GEMINI_EMBEDDING_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def get_embedding(text: str, chunk_size: int = 800):
    try:
        if not text or text.strip() == "":
            logger.error("Empty text provided for embedding")
            return None

        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        all_embeddings = []

        for chunk in chunks:
            response = client.embeddings.create(
                model="gemini-embedding-001",
                input=chunk
            )
            all_embeddings.append(response.data[0].embedding)

        if len(all_embeddings) == 1:
            return all_embeddings[0]

        return all_embeddings

    except Exception as e:
        logger.error(
            "Gemini embedding failed",
            extra={"error": str(e)}
        )
        return None
