import os
import requests
from src.services.logger_service import logger

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsdata.io/api/1/latest"

EXCLUDE_FIELDS = (
    "source_id,source_url,source_icon,source_priority,"
    "creator,image_url,video_url,ai_tag,sentiment,sentiment_stats,"
    "ai_region,ai_org,duplicate,ai_summary,language"
)

def fetch_news(max_articles=25):
    try:
        url = (
            f"{BASE_URL}?apikey={NEWS_API_KEY}"
            f"&language=en&removeduplicate=1&excludefield={EXCLUDE_FIELDS}"
        )

        articles = []
        next_page = None

        while len(articles) < max_articles:
            final_url = url if not next_page else f"{url}&page={next_page}"

            res = requests.get(final_url, timeout=10)
            if res.status_code != 200:
                logger.error("News API failed", extra={"status": res.status_code})
                break

            data = res.json()

            results = data.get("results", [])
            if not results:
                break

            articles.extend(results)

            next_page = data.get("nextPage")
            if not next_page:
                break


        return articles[:max_articles]

    except Exception as e:
        logger.error(f"Error fetching news articles{e}")
        return []
