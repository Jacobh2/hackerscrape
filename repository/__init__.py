from objects.article import Article
from typing import List

import sqlite3


class Repository(object):

    QUERY__ARTICLE_PUT = "INSERT INTO article VALUES (:header, :author, :created, :points, :link, :num_comments);"
    QUERY_ARTICLE_GET = "SELECT header, author, created, points, link, num_comments FROM article"

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)

    def put_article(self, articles: List[Article]) -> bool:
        try:
            with self.conn as cur:
                cur.executemany(self.QUERY__ARTICLE_PUT, list(map(Article._asdict, articles)))
            return True
        except Exception:
            # TODO: Log and raise
            pass
        return False

    def get_article(self) -> List[Article]:
        try:
            with self.conn as cur:
                cur.execute(self.QUERY_ARTICLE_GET)
                raw_articles = cur.fetchall()
                return list(map(lambda a: Article(*a), raw_articles))
        except Exception:
            # TODO: Log and raise
            pass
        return None
