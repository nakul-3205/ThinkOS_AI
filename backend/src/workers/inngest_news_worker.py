from inngest import Inngest
from src.services.logger_service import logger
from src.services.news import fetch_news
from src.services.embedder import get_embedding
from src.clients.qdrant_news_client import qdrant_client,NEWS_COLLECTION
from datetime import datetime

inngest_client=Inngest(app_id="thinkos-Ai-news-worker")
qdrant=qdrant_client
@inngest_client.create_function(
    fn_id="daily_news_upload",
    trigger=Inngest.TriggerCron(cron="TZ=Asia/Kolkata 0 9 * * *")  # 9 AM IST
)
async def dail_news_inngest(ctx: Inngest.Context)-> None:
    try:
        articles=fetch_news(max_articles=25)
        if not articles:
            return
        
        events=[
        {
            "name": "thinkos/news.embed.upsert",
            "data": {
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "content": article.get("content", ""),
                "keywords": article.get("keywords", []),
                "category": article.get("category", []),
                "country": article.get("country", []),
            }}
        for article in articles
        ]
        await ctx.step.send_event("news-embedding-events", events)
    except Exception as e:
            logger.error(f"Inngest worker for news upload failed{e}")
            return None
        
@inngest_client.create_function(
    fn_id="news-embed-upsert",
    trigger=Inngest.TriggerEvent(event="thinkos/news.embed.upsert")
)
async def embed_and_upsert(ctx: Inngest.Context) -> None:
    try:
        data = ctx.event.data
        combined_text = f"{data['title']}\n\n{data['description']}\n\n{data.get('content','')}"
        embedding = get_embedding(combined_text)
        if embedding:
         qdrant.upsert(
            collection_name=NEWS_COLLECTION,
            points=[{
                "id": data["article_id"],
                "vector": embedding,
                "payload": {
                    "title": data["title"],
                    "description": data["description"],
                    "content": data.get("content", ""),
                    "keywords": data.get("keywords", []),
                    "category": data.get("category", []),
                    "country": data.get("country", []),
                    "datatype": data.get("datatype", ""),
                    "pubDate": data.get("pubDate"),
                    "source_name": data.get("source_name", ""),
                    "stored_at": datetime.utcnow().isoformat()
                }
            }]
        )
    except Exception as e:
            logger.error(f"Inngest worker for news upload failed{e}")
            return None

@inngest_client.create_function(
    fn_id="news-cleanup",
    trigger=Inngest.TriggerCron(cron="TZ=Asia/Kolkata 0 3 * * *")
)
async def cleanup_old_news(ctx: Inngest.Context) -> None:
    from datetime import timedelta
    limit_date = datetime.utcnow() - timedelta(days=30)

    to_delete = qdrant.scroll(
        collection_name=NEWS_COLLECTION,
        limit=500,
        with_payload=True
    )

    delete_ids = []
    for point in to_delete[0]:
        stored_at = point.payload.get("stored_at")
        if stored_at and datetime.fromisoformat(stored_at) < limit_date:
            delete_ids.append(point.id)

    if delete_ids:
        qdrant.delete(
            collection_name=NEWS_COLLECTION,
            points=delete_ids
        )