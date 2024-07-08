import toml

from loguru import logger

def load_config():
    try:
        config = toml.load('settings/config.toml')
        return config
    except Exception as e:
        logger.error(f'Failed to load config file with error: {str(e)}')