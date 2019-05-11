from objects.article import Article
from typing import List

import sqlite3


class Repository(object):

    QUERY__ARTICLE_PUT = "INSERT INTO article VALUES (?, ?, ?, ?, ?, ?);"
    QUERY_ARTICLE_GET = "SELECT * FROM article"

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)

    def put_article(self, articles: List[Article]) -> bool:
        ret = False
        try:
            with self.conn as cur:
                cur.executemany(self.QUERY__ARTICLE_PUT, list(map(tuple, articles)))
            ret = True
        except Exception:
            pass
        return ret

    def get_article(self) -> List[Article]:
        articles = None
        try:
            with self.conn as cur:
                cur.execute(self.QUERY_ARTICLE_GET)
                articles = cur.fetchall()
        except Exception:
            pass
        return articles
