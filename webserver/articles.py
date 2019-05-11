import logging
import http
from os import environ

from aiohttp import web

from repository import Repository


repository = Repository(environ['DB_NAME'])


route = web.RouteTableDef()

logger = logging.getLogger('HTTP-Articles')

@route.get('/articles')
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
