import logging
import http
from os import environ

from aiohttp import web
from aiohttp.http_exceptions import HttpProcessingError

from repository import Repository
from scrape import ScrapeManager
from ranker import HeaderRanker


repository = Repository(environ["DB_NAME"])
repository.create_table()

scrape_manager = ScrapeManager()

header_ranker = HeaderRanker()


route = web.RouteTableDef()

logger = logging.getLogger("HTTP-Articles")


@route.get("/articles")
async def get_ranked_articles(request):
    global repository
    logger.info("Client requests ranked articles")

    # Ask repository for articles
    articles = repository.get_article()
    logger.info("Found %s articles", len(articles))

    if not articles:
        raise HttpProcessingError(message="", code=http.HTTPStatus.NO_CONTENT)

    # Run ranker given the articles
    ranked_articles = header_ranker.rank(articles)

    # Format them for a json response
    ranked_articles = list(map(lambda a: a._asdict(), ranked_articles))

    # Return!
    return web.json_response({"ok": True, "data": ranked_articles})


@route.put("/articles")
async def save_new_articles(request):
    global repository
    logger.info("Client requests to save new articles")

    # Scrape the site
    articles = scrape_manager.scrape()

    # Save the articles
    save_ok = repository.put_article(articles)

    if not save_ok:
        raise HttpProcessingError(
            message="Failed to save articles",
            code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    # Return!
    return web.json_response({"ok": True})
