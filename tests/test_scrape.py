from pytest import fixture

from objects import article
import scrape


@fixture
def content():
    return """
        <html>
            <a class="storylink" href="url1">Title one</a>
            <a class="storylink" href="url2">Title two</a>
        </html>
        """


@fixture
def articles():
    return [
        article.Article("Title one", "Anonymous", "1970-01-01", 1, "url1", 0),
        article.Article("Title two", "Anonymous", "1970-01-01", 1, "url2", 0),
    ]


class TestScrapeManager(object):
    def test_scrape(self, content, articles):
        # setup content for article

        # Call code
        scrape_manager = scrape.ScrapeManager(lambda u: content)
        articles = scrape_manager.scrape()

        # Assert
        assert articles == articles


# TODO: Make sure to send in content_provider where
# ScarpeManager is used: requests.get(url).text
