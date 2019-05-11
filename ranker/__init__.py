from objects import Article
from typing import List, Protocol


class Ranker(object):
    def rank(self, articles: List[Article]) -> List[Article]:
        raise NotImplementedError


class DateRanker(Ranker):
    def rank(self, articles: List[Article]) -> List[Article]:
        return sorted(articles, key=lambda article: article.date, reverse=True)


class ScoreRanker(Ranker):
    def rank(self, articles: List[Article]) -> List[Article]:
        return sorted(articles, key=lambda article: article.score, reverse=True)
