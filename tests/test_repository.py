from unittest.mock import MagicMock
from pytest import fixture

import repository
from objects import article


@fixture
def articles():
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
def my_repository(articles):
    rep = repository.Repository("my_db_name")
    rep._get_connection = MagicMock()
    rep._get_connection().__enter__().cursor().fetchall.return_value = list(
        map(tuple, articles)
    )
    return rep


class TestRepository(object):
    def test_get_article(self, articles, my_repository):
        # Set up data for test

        # Run code
        received_articles = my_repository.get_article()

        # Assert
        assert received_articles == articles
