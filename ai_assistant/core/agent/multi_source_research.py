import requests
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup

class MultiSourceResearch:
    def search_duckduckgo(self, query, max_results=3):
        return [r["body"] for r in DDGS().text(query, max_results=max_results)]

    def search_wikipedia(self, query):
        url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            return " ".join([p.get_text() for p in soup.find_all("p")[:2]])
        return None

    def gather(self, query):
        results = []
        results.extend(self.search_duckduckgo(query))
        wiki = self.search_wikipedia(query)
        if wiki:
            results.append(wiki)
        return results
