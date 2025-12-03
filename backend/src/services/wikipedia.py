import wikipediaapi

wiki = wikipediaapi.Wikipedia(
    user_agent='ThinkOS Ai',
    language='en'
)

def fetch_wiki_page(title: str):
    page = wiki.page(title)
    if not page.exists():
        return {"exists": False}

    return {
        "exists": True,
        "title": page.title,
        "summary": page.summary,
        "content": page.text,
        "fullurl": page.fullurl,
        "canonicalurl": page.canonicalurl,
        "categories": list(page.categories.keys()),
        "links": list(page.links.keys()),
        "datatype": "wikipedia"
    }
