import logging
import http
from os import environ

from aiohttp import web
from aiohttp.http_exceptions import HttpProcessingError

from repository import Repository


repository = Repository(environ["DB_NAME"])


route = web.RouteTableDef()

logger = logging.getLogger("HTTP-Articles")


@route.get("/articles")
async def get_ranked_articles(request):
    global repository
    logger.info("Client requests ranked articles")

    # Ask repository for articles
    articles = repository.get_article()
    logger.info("Found %s articles", len(articles))

    # Format them for a json response
    articles = list(map(lambda a: a._asdict(), articles))

    # Return!
    return web.json_response({"ok": True, "data": articles})


@route.put("/articles")
async def save_new_articles(request):
    global repository
    logger.info("Client requests to save new articles")

    ## TBI: Call scraper to get new articles!

    # Return!
    return web.json_response({"ok": True})
