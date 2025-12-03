import os 
from tavily import TavilyClient
import requests
from src.services.logger_service import logger
API_KEY=os.getenv('TAVILY_API_KEY')
client=TavilyClient(API_KEY)

def tavily_search(query:str,mode:str="basic",depth: str="basic",max_results:int=5):
    try:

        response=client.search(
            query=query,
            include_answer=mode,
            search_depth=depth,
            max_results=max_results,
        )

        return response
    except Exception as e:
        logger.error(f"Tavily api error{e}")
        return {"results":[],"error":"tavily failed"}