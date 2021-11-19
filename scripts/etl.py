"""This modules implement the class ExchangeETL responsible
to make all transformations in the dataframe and create and export
the plots 
"""
import pandas as pd
import numpy as np
from pathlib import Path
import logging
from .utils import set_logger, parse_config

class ExchangeETL():

    config_path: str 
    data_path: str 
    dataframe : pd.DataFrame
    logger : logging
    config : dict

    def __init__(self, config_path: str) -> None:
        self.config_path = config_path
        self.data_path = None
        self.dataframe = None
        self.logger = None
        self.config = None


    def load_dataframe(self, data_path: str) -> None:
        self.dataframe = pd.read_csv(data_path)

    def raname_columns(self, columns: dict) -> None: 
        self.dataframe.rename(columns, inplace= True)

    def change_column_type(self, column: str, type: str) -> None:
        try:
            if type == 'datetime':
                self.dataframe[column] = pd.to_datetime(self.dataframe[column])

            elif type == 'numeric':
                self.dataframe[column] = pd.to_numeric(self.dataframe[column])

        except:
            self.logger.warning(
                "%s is not a valid type. The change in the column type was not performed", type)


    def processing(self):

        # load config from config file
        self.config = parse_config(self.config_path)

        # configure logger
        self.logger = set_logger(self.config['log']['log_path'])
        self.logger.info("Load config from %s", self.config_path)

        # obtaining data path from config file
        self.data_path = self.config['etl']['raw_data_path']
        self.logger.info("ETL config: %s", self.config['etl'])

        # beginning the data transformation
        self.logger.info(
        "-------------------Start data transformation-------------------")
        self.load_dataframe()
        self.logger.info("The dataset was loaded.")

        # renaming the columns

        # dropping columns
