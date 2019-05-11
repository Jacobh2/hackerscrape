from pytest import fixture

import ranker
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


class TestRanker(object):
    def test_created_ranker(self, articles):

        wanted_result = [a.created for a in articles]
        wanted_result.sort(reverse=True)

        # Create the object which to test
        created_ranker = ranker.CreatedRanker()
        ranked_articles = [a.created for a in created_ranker.rank(articles)]

        # Assert
        assert ranked_articles == wanted_result

    def test_point_ranker(self, articles):

        wanted_result = [article.points for article in articles]
        wanted_result.sort(reverse=True)

        # Create the object which to test
        created_ranker = ranker.PointRanker()
        ranked_articles = [a.points for a in created_ranker.rank(articles)]

        # Assert
        assert ranked_articles == wanted_result

    def test_header_ranker(self, articles):

        wanted_result = [a.header for a in articles]
        wanted_result.sort()

        # Create the object which to test
        created_ranker = ranker.HeaderRanker()
        ranked_articles = [a.header for a in created_ranker.rank(articles)]

        # Assert
        assert ranked_articles == wanted_result
