from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup

from objects.article import Article


class ScrapeManager(object):
    URL = "https://news.ycombinator.com/newest"

    def __init__(self, content_provider):
        self.content_provider = content_provider

    def scrape(self) -> List[Article]:
        """Scrapes the first page of Hacker News."""
        content = self.content_provider(self.URL)
        return self._parse(content)

    def _parse(self, content: str) -> List[Article]:
        soup = BeautifulSoup(content, "html.parser")
        titles = soup.find_all("a", "storylink")
        return [
            Article(
                header=x.text,
                author="Anonymous",
                created="1970-01-01",
                points=1,
                link=x["href"],
                num_comments=0,
            )
            for x in titles
        ]
