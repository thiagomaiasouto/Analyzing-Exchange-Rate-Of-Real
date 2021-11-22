"""
This module implements all the tests
"""
import pandas as pd
import numpy as np
from scripts.etl import ExchangeETL
from scripts.utils import set_logger, parse_config


def validate_columns(new_columns: dict,
                     columns: pd.Index,
                     valid: bool) -> bool:
    """
    This function is responsible to validate the columns of a DataFrame
    Args:
        new_columns (dict): specify the columns that were changed
        columns (pd.Index): indicate the new columns of the DataFrame
        valid (bool): indicate if the function responsible to change the columns worked.
    Return:
        bool : indicate if the test pass or fail
    """

    return set(new_columns.values()).issubset(set(columns)) and valid


def validate_type(dtype: np.dtype,
                  valid: bool,
                  cols_type: np.dtype) -> bool:
    """
    This function is responsible to validate the columns type of a DataFrame
    Args:
        dtype (np.dtype): specify the dtype of the column
        valid (bool): indicate if the function responsible to change the columns worked.
        cols_type (np.dtype): indicate the new column dtype of the DataFrame
    Return:
        bool : indicate if the test pass or fail
    """

    return (cols_type == dtype) and valid


def test_set_logger():
    """
    This function performs the test of the set_logger function
    """
    log_path = "./log/etl.log"
    logger = set_logger(__name__,log_path)
    assert logger is not None


def test_parse_config():
    """
    This function performs the test of the parse_config function
    """
    config_path = "./config.yml"
    config = parse_config(config_path)
    assert isinstance(config, dict)


def test_load_dataframe():
    """
    This function performs the test of the load_dataframe function
    """
    data_path = './test/data_tests/euro-daily-hist_1999_2020.csv'
    etl = ExchangeETL()
    assert etl.load_dataframe(0, data_path)


def test_rename_columns():
    """
    This function performs the test of the rename_columns function
    """
    data_path = './test/data_tests/euro-daily-hist_1999_2020.csv'
    etl = ExchangeETL()
    etl.load_dataframe(0, data_path)
    old_columns = etl.dataframes[0].columns
    new_column = {old_columns[0]: "test_column"}
    valid = etl.rename_columns(0, new_column)
    assert validate_columns(new_column, etl.dataframes[0].columns, valid)


def test_change_column_type_datetime():
    """
    This function performs the test of the change_column_type function
    """
    data_path = './test/data_tests/euro-daily-hist_1999_2020.csv'
    etl = ExchangeETL()
    etl.load_dataframe(0, data_path)
    column = etl.dataframes[0].columns[0]
    mtype = 'datetime'
    dtype = np.datetime64
    valid = etl.change_column_type(0, column, mtype)
    assert validate_type(dtype, valid, etl.dataframes[0].dtypes[column].type)
