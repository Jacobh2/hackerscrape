from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup

from objects.article import Article


class ScrapeManager(object):
    URL = "https://news.ycombinator.com/newest"

    def scrape(self) -> List[Article]:
        """Scrapes the first page of Hacker News."""
        content = self._get(self.URL)
        return self._parse(content)

    def _parse(self, content: str) -> List[Article]:
        soup = BeautifulSoup(content, "html.parser")
        titles = soup.find_all("a", "storylink")
        return [
            Article(
                header=x.text,
                author="Anonymous",
                created=datetime.now(),
                points=1,
                link=x["href"],
                num_comments=0,
            )
            for x in titles
        ]

    def _get(self, url: str) -> str:
        return requests.get(url).text
