from qdrant_client import QdrantClient
import os

QDRANT_HOST_API_KEY=os.getenv('QDRANT_NEWS_API_KEY')
QDRANT_HOST_API_HOST=os.getenv('QDRANT_NEWS_URL')

qdrant_client = QdrantClient(
    host=QDRANT_HOST_API_HOST,
    api_key=QDRANT_HOST_API_KEY,
)
NEWS_COLLECTION = "daily_news_vectors"