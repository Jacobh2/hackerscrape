from pytest import fixture
from unittest.mock import MagicMock

import service
from ranker import HeaderRanker
from objects import article


@fixture
def articles_database():
    return [
        article.Article(
            header="What happens next",
            author="Sven",
            created="2019-05-05",
            points=10,
            link="www.url.com",
            num_comments=5,
        ),
        article.Article(
            header="A thing happend next",
            author="Adam",
            created="2014-01-25",
            points=-4,
            link="www.a-url.com",
            num_comments=0,
        ),
        article.Article(
            header="Zoo animal escapes :O",
            author="Zorro",
            created="2019-10-05",
            points=99,
            link="www.zoo-info.com",
            num_comments=1760,
        ),
        article.Article(
            header="Beyond what happens next",
            author="Urgel",
            created="2018-07-05",
            points=50,
            link="www.urgels-blog.com",
            num_comments=10,
        ),
    ]


@fixture
def articles_ranked():
    return [
        article.Article(
            header="A thing happend next",
            author="Adam",
            created="2014-01-25",
            points=-4,
            link="www.a-url.com",
            num_comments=0,
        ),
        article.Article(
            header="Beyond what happens next",
            author="Urgel",
            created="2018-07-05",
            points=50,
            link="www.urgels-blog.com",
            num_comments=10,
        ),
        article.Article(
            header="What happens next",
            author="Sven",
            created="2019-05-05",
            points=10,
            link="www.url.com",
            num_comments=5,
        ),
        article.Article(
            header="Zoo animal escapes :O",
            author="Zorro",
            created="2019-10-05",
            points=99,
            link="www.zoo-info.com",
            num_comments=1760,
        ),
    ]


@fixture
def articles_ranked_serialized(articles_ranked):
    return list(map(lambda a: a._asdict(), articles_ranked))


class MockRanker(object):
    def __init__(self, articles_ranked):
        self.articles_ranked = articles_ranked

    def rank(self, input_articles):
        return self.articles_ranked


@fixture
def test_ranker(articles_ranked):
    return MockRanker(articles_ranked)


@fixture
def hacker_scrape(test_ranker, articles_database):
    repository = MagicMock(name="repository")
    repository.get_article.return_value = articles_database

    scrape_manager = MagicMock(name="scrape_manager")

    return service.HackerScrape(repository, scrape_manager, test_ranker)


class TestHackerScrape(object):
    def test_get_ranked_articles(
        self, hacker_scrape, articles_ranked, articles_ranked_serialized
    ):
        # Run code
        returned_articles = hacker_scrape.get_ranked_articles()

        # assert
        assert returned_articles == articles_ranked_serialized

    def test_save_new_article(self, hacker_scrape):
        my_empty_list = list()
        hacker_scrape.scrape_manager.scrape.return_value = my_empty_list

        ret = hacker_scrape.save_new_articles()

        hacker_scrape.repository.put_article.assert_called_once_with(my_empty_list)
