import pytest
from scripts.etl import ExchangeETL
from scripts.utils import set_logger, parse_config


def test_set_logger():
    log_path = "./log/etl.log"
    logger = set_logger(log_path)
    assert logger is not None

def test_parse_config():
    config_path = "./config.yml"
    config = parse_config(config_path)
    assert isinstance(config, dict)

def test_load_dataframe():
    data_path = './data/euro-daily-hist_1999_2020.csv'
    config_path = "./config.yml"
    ETL = ExchangeETL(config_path)
    ETL.load_dataframe(data_path)
    assert ETL.dataframe is not None

