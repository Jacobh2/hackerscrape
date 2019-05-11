from abc import abstractmethod
from objects.article import Article
from typing import List, Protocol


class Ranker(Protocol):
    @abstractmethod
    def rank(self, articles: List[Article]) -> List[Article]:
        pass


class DateRanker(object):
    def rank(self, articles: List[Article]) -> List[Article]:
        return sorted(articles, key=lambda article: article.created, reverse=True)


class ScoreRanker(object):
    def rank(self, articles: List[Article]) -> List[Article]:
        return sorted(articles, key=lambda article: article.points, reverse=True)
