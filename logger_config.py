import logging
import logging.config

import yaml
import os


def setup(log_output=None, logging_config_path='/usr/src/app/logging.yaml', only_std_out_level=None):

    logger = logging.getLogger("App")

    if only_std_out_level is not None:
        # Setup to only put to stdout
        logging.basicConfig(
            level=only_std_out_level,
            format="%(asctime)s#%(levelname)-7s:%(threadName)-10s:%(name)-10s:%(funcName) -35s:%(lineno) -5d:%(message)s"
            )
        return logger

    if os.path.exists(logging_config_path):
        with open(logging_config_path) as f:
            config = yaml.load(f)
        
        # Modify the config if we're given a name!
        if log_output is not None:
            config['handlers']['mtlog']['name'] = log_output

        logging.config.dictConfig(config)

    return logger
