import asyncio
from os import environ
from aiohttp import web
import requests

import logger_config
logger = logger_config.setup(log_output=environ.get("LOG_OUTPUT"))

# We want to config the logging before loading anything else
from webserver import app

from service import HackerScrape
from repository import Repository
from scrape import ScrapeManager
from ranker import HeaderRanker


def exception_handler(loop, context):
    logger.warning("Ok, so we crashed somewhere: %s", context)


async def create_webserver(loop, address, port, propagate_error, hacker_scrape):
    logger.info("Starting HTTP")
    webapp = app.setup_web(propagate_error, hacker_scrape)
    runner = web.AppRunner(webapp)
    await runner.setup()
    site = web.TCPSite(runner, address, port)
    await site.start()


def setup_hacker_scrape(db_name):
    content_provider = lambda url: requests.get(url).text
    repository = Repository(db_name)
    repository.create_table()
    
    scrape_manager = ScrapeManager(content_provider)
    ranker = HeaderRanker()
    return HackerScrape(repository, scrape_manager, ranker)


def main(loop, db_name, address, port, propagate_error):

    hacker_scrape = setup_hacker_scrape(db_name)
    
    logger.info("Creating HTTP task")
    loop.create_task(create_webserver(loop, address, port, propagate_error, hacker_scrape))

    logger.info("Waiting...")
    loop.run_forever()


if __name__ == "__main__":
    address = environ.get('ADDRESS', '0.0.0.0')
    port = int(environ.get('PORT', 80))
    propagate_error = bool(int(environ.get('API_PROPAGATE_500_ERRORS', 0)))
    db_name = environ['DB_NAME']

    logger.info("Starting main!")
    loop = asyncio.get_event_loop()
    
    # Set the debug log for the event loop only if the level is set to debug
    loop.set_debug(environ.get('LOG_LEVEL', 'WARNING').strip().lower() == 'debug')

    loop.set_exception_handler(exception_handler)

    main(loop, db_name, address, port, propagate_error)
