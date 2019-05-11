import logging
import logging.config

import yaml
import os


def setup(log_output=None, logging_config_path='/usr/src/app/logging.yaml'):

    logger = logging.getLogger("App")

    if os.path.exists(logging_config_path):
        with open(logging_config_path) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        
        # Modify the config if we're given a name!
        if log_output is not None:
            config['handlers']['mtlog']['name'] = log_output

        logging.config.dictConfig(config)

    return logger
