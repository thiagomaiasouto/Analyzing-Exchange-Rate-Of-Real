"""This modules implement the class ExchangeETL responsible
to make all transformations in the dataframe and create and export
the plots
"""
from typing import List
from pathlib import Path
import logging
import pandas as pd
from .utils import set_logger, parse_config


class ExchangeETL():
    """
    This class implements a ETL pipeline
    """

    config_path: str
    data_path: str
    dataframes: List[pd.DataFrame]
    logger: logging
    config: dict

    def __init__(self, config_path: str = "./config.yml") -> None:
        """
        This is the constructor of the class ExchangeETL
        and is responsible for initializing the attributes of the object.
        Args:
        config_file [str]: path to the config yaml file
        Returns:
        None
        """

        # initializing the config_path attribute
        self.config_path = config_path

        # loading config file in the config attribute
        self.config = parse_config(self.config_path)

        # configuring logger attribute
        self.logger = set_logger(
            "ExchangeETL",
            self.config['log']['log_etl_path'])
        self.logger.info("Load config from %s", self.config_path)
        self.logger.info("ETL config: %s", self.config['etl'])

        # initializing the data_path atribute as None
        self.data_path = None

        # creating the dataframes list as None
        self.dataframes = [pd.DataFrame() for i in range(3)]

    def load_dataframe(self, index: int, data_path: str) -> bool:
        """
        This function is responsible to validate the inputs, for
        load the dataframe in a attribute and returns True if
        executes successfully;
        Args:
            index (int): index for indentifie the dataframe in the dataframe list.
            data_path (str): indicates the path for the dataframe.
        Returns:
            bool: indicates if the function worked well or not.
        """
        try:
            assert isinstance(data_path, str)
            self.dataframes[index] = pd.read_csv(data_path)
            self.logger.info("The dataset was loaded.")
            return True
        except Exception as exception:
            self.logger.error("%s", exception)
            self.logger.warning(
                "The dataset in path %s was not loaded.", data_path)
            return False

    def rename_columns(self, index: int, columns: dict) -> bool:
        """
        This function is responsible to validate the inputs, for
        rename columns of a dataframe and returns True if
        executes successfully;
        Args:
            index (int): index for indentifie the dataframe in the dataframe list.
            columns (dict): indicates the columns will be renamed.
        Returns:
            bool: indicates if the function worked well or not.
        """
        try:
            assert isinstance(columns, dict)
            self.dataframes[index].rename(columns=columns, inplace=True)
            return True
        except Exception as exception:
            self.logger.error("%s", exception)
            self.logger.warning("The column's names was not changed.")
            return False

    def change_column_type(self, index: int, column: str, dtype: str) -> None:
        """
        This function is responsible to validate the inputs, for
        change the column type of a dataframe and returns True if
        executes successfully;
        Args:
            index (int): index for indentifie the dataframe in the dataframe list.
            column (str): specify what column will be changed.
            type (str): indicates the new type of the column
        Returns:
            bool: indicates if the function worked well or not.
        """
        try:
            if dtype == 'datetime':
                self.dataframes[index][column] = pd.to_datetime(
                    self.dataframes[index][column])
                return True

            self.logger.warning("The type used was not valid")
            return False
        except Exception as exception:
            self.logger.error("%s", exception)
            self.logger.warning(
                "The change in the column type was not performed")
            return False

    def processing(self) -> None:
        """
        This method implements the processing pipeline for the ETL operations
        and export the processed dataframe
        """

        # beginning the data transformation
        self.logger.info(
            "------------Start data transformation on dataframe 0-----------")

        # loading the data path with dataframe1 path
        self.data_path = self.config['etl']['dataframe1_path']

        # loadind the dataframe0
        self.load_dataframe(0, self.data_path)
        self.logger.info("The dataframe0 was successfully loaded.")

        # droping the first row of dataframe0
        self.dataframes[0].drop(axis=0, index=0, inplace=True)
        self.logger.info("The first index of the dataframe0 was removed.")

        # copying just the columns 'Date' and 'BRL' to the dataframe0
        self.dataframes[0] = self.dataframes[0][['Date', 'BRL']]
        self.logger.info(
            "The columns 'Date' and 'BRL' from dataframe0 was selected.")

        # converting the column 'Date' of dataframe0 to datetime
        self.change_column_type(0, 'Date', 'datetime')
        self.logger.info(
            "The type of the column 'Date' of dataframe0 was changed to datetime type.")

        # converting the column 'BRL' of dataframe0 to float
        self.dataframes[0]['BRL'] = self.dataframes[0]['BRL'].astype(float)
        self.logger.info(
            "The type of the column 'BRL' of dataframe0 was changed to float type.")

        self.logger.info(
            "------------Start data transformation on dataframe 1-----------")

        # loading the data path with dataframe2 path
        self.data_path = self.config['etl']['dataframe2_path']

        # loadind the dataframe1
        self.load_dataframe(1, self.data_path)
        self.logger.info("The dataframe1 was successfully loaded.")

        # renaming the columns of dataframe1
        columns = {'BRAZIL - REAL/US$': 'BRL',
                   'Time Serie': 'Date'}
        self.rename_columns(1, columns)
        self.logger.info("The columns of dataframe1 was successfully changed.")

        # converting the column 'Date' of dataframe1 to datetime
        self.change_column_type(1, 'Date', 'datetime')
        self.logger.info(
            "The type of the column 'Date' of dataframe1 was changed to datetime type.")

        # sorting the values of column 'Date' of dataframe1
        self.dataframes[1].sort_values('Date', inplace=True, ascending=False)
        self.logger.info(
            "The values of dataframe1 was successfully sorted by values in column 'Date'.")

        # reseting the index of dataframe1
        self.dataframes[1].reset_index(drop=True, inplace=True)
        self.logger.info("The index of dataframe1 was reseting successfully.")

        # copying just the columns 'Date' and 'BRL' to the dataframe1
        self.dataframes[1] = self.dataframes[1][['Date', 'BRL']]
        self.logger.info(
            "The columns 'Date' and 'BRL' from dataframe1 was selected.")

        # applying date filter in dataframe1
        filter1 = self.dataframes[1]['Date'].dt.year > 1994
        filter2 = self.dataframes[1]['Date'].dt.year < 2009
        self.dataframes[1] = self.dataframes[1][filter1 & filter2]
        self.logger.info(
            "The interval between 1994-2009 was filtered in dataframe1.")

        # applying date filter in dataframe0
        filter3 = self.dataframes[0]['Date'].dt.year > 2008
        self.dataframes[0] = self.dataframes[0][filter3]
        self.logger.info("The dates above 2008 was filtered in dataframe0.")

        # removing lines with ND value in dataframe1
        filter4 = self.dataframes[1]['BRL'] == 'ND'
        self.dataframes[1].drop(
            self.dataframes[1][filter4].index,
            inplace=True)
        self.logger.info(
            "The rows with Non Data was removed from dataframe1 successfully.")

        # concatenating dataframe0 and dataframe1
        self.dataframes[2] = pd.concat(
            [self.dataframes[0], self.dataframes[1]])
        self.logger.info(
            "The dataframe0 and dataframe1 was concatenated in dataframe2.")

        # filtering dates above 2000 in dataframe2
        filter5 = self.dataframes[2]['Date'].dt.year >= 2000
        self.dataframes[2] = self.dataframes[2][filter5]
        self.logger.info("The dates above 2000 was filtered in dataframe2.")

        # exporting the transformed dataset
        processed_path = Path(self.config['etl']['processed_path'])
        self.dataframes[2].to_csv(processed_path, index=False)
        self.logger.info("The transformed dataset was exported successfully.")
