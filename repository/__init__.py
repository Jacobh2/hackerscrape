from objects.article import Article
from typing import List
import logging

import sqlite3


logger = logging.getLogger("Database")


class Repository(object):

    QUERY_ARTICLE_CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS article (
        header       TEXT    NOT NULL,
        author       TEXT    NOT NULL,
        created      TEXT    NOT NULL,
        points       INTEGER NOT NULL,
        link         TEXT    NOT NULL,
        num_comments INTEGER NOT NULL
    );"""
    QUERY_ARTICLE_PUT = "INSERT INTO article VALUES (:header, :author, :created, :points, :link, :num_comments);"
    QUERY_ARTICLE_GET = "SELECT header, author, created, points, link, num_comments FROM article"

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)

    def create_table(self):
        try:
            with self.conn as cur:
                cur.execute(self.QUERY_ARTICLE_CREATE_TABLE)
        except Exception:
            logger.exception("Failed to create table")
            raise

    def put_article(self, articles: List[Article]) -> bool:
        try:
            with self.conn as cur:
                cur.executemany(self.QUERY_ARTICLE_PUT, list(map(Article._asdict, articles)))
            return True
        except Exception:
            logger.exception("Failed to save articles")
            raise

    def get_article(self) -> List[Article]:
        try:
            with self.conn as cur:
                cur.execute(self.QUERY_ARTICLE_GET)
                raw_articles = cur.fetchall()
                return list(map(lambda a: Article(*a), raw_articles))
        except Exception:
            logger.exception("Failed to get articles")
            raise
