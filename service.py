import logging

from repository import Repository
from scrape import ScrapeManager
from ranker import Ranker


class HackerScrape(object):
    def __init__(
        self, repository: Repository, scrape_manager: ScrapeManager, ranker: Ranker
    ):
        self.logger = logging.getLogger("HackerScrape")

        self.repository = repository
        self.scrape_manager = scrape_manager
        self.ranker = ranker

    def get_ranked_articles(self):
        self.logger.info("Client requests ranked articles")

        # Ask repository for articles
        articles = self.repository.get_article()
        self.logger.info("Found %s articles", len(articles))

        if not articles:
            return None

        # Run ranker given the articles
        ranked_articles = self.ranker.rank(articles)

        # Format them for a json response
        return list(map(lambda a: a._asdict(), ranked_articles))

    def save_new_articles(self):
        self.logger.info("Client requests to save new articles")

        # Scrape the site
        articles = self.scrape_manager.scrape()

        # Save the articles
        return self.repository.put_article(articles)
