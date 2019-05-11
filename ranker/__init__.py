from abc import abstractmethod
from objects.article import Article
from typing import List, Protocol


class Ranker(Protocol):
    @abstractmethod
    def rank(self, articles: List[Article]) -> List[Article]:
        pass


class CreatedRanker(object):
    def rank(self, articles: List[Article]) -> List[Article]:
        return sorted(articles, key=lambda article: article.created, reverse=True)


class PointRanker(object):
    def rank(self, articles: List[Article]) -> List[Article]:
        return sorted(articles, key=lambda article: article.points, reverse=True)


class HeaderRanker(object):
    def rank(self, articles: List[Article]) -> List[Article]:
        return sorted(articles, key=lambda article: article.header, reverse=True)
