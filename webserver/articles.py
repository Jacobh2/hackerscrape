import logging
import http

from aiohttp import web
from aiohttp.http_exceptions import HttpProcessingError

route = web.RouteTableDef()


class ArticleRoute(object):
    def __init__(self, hacker_scrape):
        self.logger = logging.getLogger("ArticleRoute")
        self.hacker_scrape = hacker_scrape

    @route.get("/articles")
    async def get_ranked_articles(self, request):
        self.logger.info("Client requests ranked articles")
        articles = self.hacker_scrape.get_ranked_articles()

        if not articles:
            raise HttpProcessingError(message="", code=http.HTTPStatus.NO_CONTENT)

        return web.json_response({"ok": True, "data": articles})

    @route.put("/articles")
    async def save_new_articles(self, request):
        logger.info("Client requests to save new articles")
        save_ok = self.hacker_scrape.save_new_articles()

        if not save_ok:
            raise HttpProcessingError(
                message="Failed to save articles",
                code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
            )

        return web.json_response({"ok": True})
