import pytest
import pandas as pd
import numpy as np
from scripts.etl import ExchangeETL
from scripts.utils import set_logger, parse_config

def validate_columns(new_columns: dict,
                      columns: pd.Index, 
                      valid : bool) -> bool:

    if ((set(new_columns.values()).issubset(set(columns)) and valid)):
        return True
    else:
        return False

def validate_type(dtype: np.dtype,
                  valid: bool,
                  cols_type: np.dtype) -> bool:
    if((cols_type == dtype) and valid):
        return True
    return False
    

def test_set_logger():
    log_path = "./log/etl.log"
    logger = set_logger(log_path)
    assert logger is not None

def test_parse_config():
    config_path = "./config.yml"
    config = parse_config(config_path)
    assert isinstance(config, dict)

def test_load_dataframe():
    data_path = './test/data_tests/euro-daily-hist_1999_2020.csv'
    ETL = ExchangeETL()
    assert ETL.load_dataframe(0, data_path)

def test_rename_columns():
    data_path = './test/data_tests/euro-daily-hist_1999_2020.csv'
    ETL = ExchangeETL()
    ETL.load_dataframe(0, data_path)
    old_columns = ETL.dataframes[0].columns
    new_column = {old_columns[0] : "test_column"}
    valid = ETL.rename_columns(0, new_column)
    assert validate_columns(new_column, ETL.dataframes[0].columns, valid)

def test_change_column_type_datetime():
    data_path = './test/data_tests/euro-daily-hist_1999_2020.csv'
    ETL = ExchangeETL()
    ETL.load_dataframe(0, data_path)
    column = ETL.dataframes[0].columns[0]
    type = 'datetime'
    dtype = np.datetime64
    valid = ETL.change_column_type(0, column, type)
    assert validate_type(dtype, valid, ETL.dataframes[0].dtypes[column].type)



