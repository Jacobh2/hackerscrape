from os import environ
import logging

from aiohttp import web

from webserver.articles import route as article_route


logger = logging.getLogger("Web")

main_route = web.RouteTableDef()

propagate_error = False


@main_route.get("/")
def index(request):
    return web.json_response({"ok": True, "msg": "tbi"})


@main_route.get("/healthz")
def health_check(request):
    # TODO: Implement the check if we're healty
    return web.json_response({"ok": True})


@main_route.get("/alive")
def alive_check(request):
    # TODO: Implement the check if we're alive
    return web.json_response({"ok": True})


async def handle_error(error, request):
    global propagate_error

    # Try to find a message
    if hasattr(error, "message"):
        error_msg = error.message
    elif hasattr(error, "description"):
        error_msg = error.description
    else:
        error_msg = str(error)

    # Try to find a code
    if hasattr(error, "code"):
        error_code = error.code
    elif hasattr(error, "status"):
        error_code = error.status
    else:
        error_code = 500

    msg = "Handling {} error {}: {} for {}".format(
        error, error_msg, error_code, request
    )
    if error_code >= 500:
        logger.exception(msg)
    else:
        logger.warning(msg)

    # Check if we should propagate the 500 errors
    if not propagate_error and error_code >= 500:
        logger.info(
            "Service is not allowed to propagate the 500 errors, will return generic response"
        )
        error_code = 500
        error_msg = "Internal Server Error"

    return web.json_response(
        data={"ok": False, "code": error_code, "error": error_msg}, status=error_code
    )


@web.middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except Exception as ex:
        return await handle_error(ex, request)


def setup_web(set_propagate_error, hacker_scrape):
    global propagate_error
    propagate_error = set_propagate_error

    app = web.Application()
    app['hacker_scrape'] = hacker_scrape

    app.middlewares.append(error_middleware)

    app.add_routes(main_route)

    app.add_routes(article_route)

    return app
