import asyncio
from os import environ
from aiohttp import web

import logger_config
from webserver import app

logger = logger_config.setup(log_output=environ.get("LOG_OUTPUT"))


def exception_handler(loop, context):
    logger.warning("Ok, so we crashed somewhere: %s", context)


async def create_webserver(loop):
    logger.info("Starting HTTP")
    runner = web.AppRunner(app.app)
    await runner.setup()
    site = web.TCPSite(runner, app.ADDRESS, app.PORT)
    await site.start()


def main(loop):
    
    logger.info("Creating HTTP task")
    loop.create_task(create_webserver(loop))

    logger.info("Waiting...")
    loop.run_forever()


if __name__ == "__main__":
    logger.info("Starting main!")
    loop = asyncio.get_event_loop()
    
    # Set the debug log for the event loop only if the level is set to debug
    loop.set_debug(environ.get('LOG_LEVEL', 'WARNING').strip().lower() == 'debug')

    loop.set_exception_handler(exception_handler)

    main(loop)
