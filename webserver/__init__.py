import os
from os import path
import logging
import importlib

logger = logging.getLogger("Web")


def register_routes(app, route_path):
    all_routes = [
        "{}.{}".format(route_path, route_name[:-3])
        for route_name in filter(
            lambda n: not n.startswith("__")
            and not n.startswith("app.py")
            and not path.isdir(path.join(route_path, n)),
            os.listdir(route_path),
        )
    ]

    logger.debug("All routes: %s", all_routes)

    for route in all_routes:
        logger.info("Loading route %s", route)
        module = importlib.import_module(route)
        app.add_routes(module.route)
