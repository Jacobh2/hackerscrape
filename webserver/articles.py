import logging
import http

from aiohttp import web
from aiohttp.http_exceptions import HttpProcessingError

route = web.RouteTableDef()

logger = logging.getLogger("ArticleRoute")


@route.get("/articles")
async def get_ranked_articles(request):
    logger.info("Client requests ranked articles")
    articles = request.app["hacker_scrape"].get_ranked_articles()

    if not articles:
        raise HttpProcessingError(message="", code=http.HTTPStatus.NO_CONTENT)

    return web.json_response({"ok": True, "data": articles})


@route.put("/articles")
async def save_new_articles(request):
    logger.info("Client requests to save new articles")
    save_ok = request.app["hacker_scrape"].save_new_articles()

    if not save_ok:
        raise HttpProcessingError(
            message="Failed to save articles",
            code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    return web.json_response({"ok": True})
