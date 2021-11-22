"""This module implements utility functions for other modules."""
import logging
from pathlib import Path
import yaml
import sys


def parse_config(config_file: str) -> dict:
    """
    This function parses the config yaml file
    Args:
        config_file [str]: path to the config yaml file
    Returns:
        config [dict]
    """
    with open(config_file, "rb") as file:
        config = yaml.safe_load(file)
    return config


def set_logger(name: str, log_path: str) -> logging:
    """
    This function configure a logger
    Args:
        log_path [str]: eg: "../log/etl.log"
    Returns:
        logger [logging object]
    """
    log_path = Path(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    # create logger with __name__
    logger = logging.getLogger(name)

    # configuring the logger level
    logger.setLevel(logging.INFO)

    # creating file handler to log INFO messages in a log file
    file_handler = logging.FileHandler(log_path, mode='w')

    # creating stream handler to log INFO messages in stdout
    console_handler = logging.StreamHandler(sys.stdout)

    # creating the formatter to log messages
    formatter = logging.Formatter(
        "%(asctime)s : %(levelname)s : %(name)s : %(message)s")

    # setting the format to the file handler
    file_handler.setFormatter(formatter)

    # setting the format to the console handler
    console_handler.setFormatter(formatter)

    # adding the file handler to the logger
    logger.addHandler(file_handler)

    # adding the console handler to the logger
    logger.addHandler(console_handler)

    return logger
